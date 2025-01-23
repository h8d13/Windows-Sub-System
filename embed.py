import sys
import subprocess
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtGui import QWindow
from PyQt6.QtCore import Qt, QProcess

class VMWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QEMU VM Controller")
        self.setGeometry(100, 100, 1024, 768)
        
        # Central widget setup
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # QEMU process and window handles
        self.qemu_process = None
        self.vm_window = None
        
        # Start QEMU with window embedding
        self.start_qemu()
        QApplication.instance().processEvents()
        time.sleep(1)  # Give QEMU time to initialize
        self.embed_vm_window()

    def start_qemu(self):
        qemu_command = [
            "qemu-system-x86_64",
            "-enable-kvm",
            "-m", "6144",
            "-cpu", "host",
            "-smp", "8",
            "-hda", "myvm.qcow2",
            "-boot", "c",
            "-net", "nic",
            "-net", "user,smb=/home/hadepop/Desktop/vm/shared",
            "-display", "gtk,window-title=QEMU-Embedded-VM",
            "-qmp", "tcp:localhost:4444,server,nowait"
        ]
        
        try:
            self.qemu_process = QProcess()
            self.qemu_process.start(qemu_command[0], qemu_command[1:])
        except Exception as e:
            print(f"Error starting QEMU: {e}")
            sys.exit(1)

    def embed_vm_window(self):
        try:
            # Find window ID using xdotool
            result = subprocess.run(
                ["xdotool", "search", "--name", "QEMU-Embedded-VM"],
                capture_output=True, text=True, timeout=5
            )
            
            if result.returncode == 0:
                win_id = result.stdout.strip()
                if win_id:
                    self._embed_window(int(win_id))
                    return
                
            print("Failed to find QEMU window. Trying alternative method...")
            self._embed_window(self.qemu_process.processId())

        except Exception as e:
            print(f"Window embedding failed: {e}")

    def _embed_window(self, win_id):
        try:
            foreign_window = QWindow.fromWinId(win_id)
            container = self.central_widget.createWindowContainer(foreign_window)
            container.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            self.layout.addWidget(container)
            foreign_window.resize(self.size())
            self.vm_window = foreign_window
        except Exception as e:
            print(f"Window embedding error: {e}")

    def resizeEvent(self, event):
        if self.vm_window:
            self.vm_window.resize(event.size().width(), event.size().height())
        super().resizeEvent(event)

    def closeEvent(self, event):
        if self.qemu_process and self.qemu_process.state() == QProcess.ProcessState.Running:
            self.qemu_process.terminate()
            self.qemu_process.waitForFinished(5000)
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VMWindow()
    window.show()
    sys.exit(app.exec())
