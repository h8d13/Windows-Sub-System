import sys
import subprocess
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtGui import QWindow
from PyQt6.QtCore import QTimer, Qt

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
        
        # QEMU process handle
        self.qemu_process = None
        self.vm_window = None
        
        # Start QEMU and setup timer to check for window
        self.start_qemu()
        self.timer = QTimer()
        self.timer.timeout.connect(self.embed_vm_window)
        self.timer.start(500)  # Check every 500ms

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
            "-display", "x11,window_title=QEMU-Embedded-VM"
        ]
        
        try:
            self.qemu_process = subprocess.Popen(qemu_command)
        except FileNotFoundError:
            print("Error: QEMU executable not found!")
            sys.exit(1)

    def embed_vm_window(self):
        try:
            # Get window ID using xwininfo
            result = subprocess.run(
                ["xwininfo", "-name", "QEMU-Embedded-VM", "-int"],
                capture_output=True, text=True, timeout=2
            )
            
            # Parse window ID from output
            for line in result.stdout.split('\n'):
                if "Window id:" in line:
                    win_id = line.split()[-1]
                    win_id = int(win_id, 16)  # Convert hex to decimal
                    self._embed_window(win_id)
                    self.timer.stop()
                    return
                    
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
            pass  # Window not ready yet

    def _embed_window(self, win_id):
        # Create QWindow from X11 window ID
        foreign_window = QWindow.fromWinId(win_id)
        
        # Create container widget
        container = self.central_widget.createWindowContainer(foreign_window)
        container.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.layout.addWidget(container)
        
        # Ensure proper resizing
        foreign_window.resize(self.size())
        self.vm_window = foreign_window

    def resizeEvent(self, event):
        if self.vm_window:
            self.vm_window.resize(event.size().width(), event.size().height())
        super().resizeEvent(event)

    def closeEvent(self, event):
        # Cleanup QEMU process on window close
        if self.qemu_process and self.qemu_process.poll() is None:
            self.qemu_process.terminate()
            self.qemu_process.wait()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VMWindow()
    window.show()
    sys.exit(app.exec())
