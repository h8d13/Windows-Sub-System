import sys
import subprocess
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtCore import QProcess, Qt

class VMContainer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QEMU VM Embedded")
        self.setGeometry(100, 100, 1024, 768)
        
        # Create container widget
        self.container = QWidget()
        self.setCentralWidget(self.container)
        self.layout = QVBoxLayout(self.container)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Ensure the widget is shown before getting window ID
        self.show()
        QApplication.processEvents()
        
        # Get the window ID of our container
        self.win_id = self.container.winId()
        print(f"Container Window ID: 0x{self.win_id:x}")
        
        # Start QEMU process
        self.start_qemu()

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
            "-display", f"sdl,window-id=0x{self.win_id:x}",
            "-nographic",
            "-vga", "none"
        ]
        
        try:
            self.process = QProcess()
            self.process.start(qemu_command[0], qemu_command[1:])
        except Exception as e:
            print(f"Error starting QEMU: {e}")
            sys.exit(1)

    def closeEvent(self, event):
        if self.process and self.process.state() == QProcess.ProcessState.Running:
            self.process.terminate()
            self.process.waitForFinished(5000)
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VMContainer()
    window.show()
    sys.exit(app.exec())
