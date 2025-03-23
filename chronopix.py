import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6 import uic

# Load the UI
class ChronoPix(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("chronopix.ui", self)

        # Connect buttons to functions
        self.selectFolderButton.clicked.connect(self.select_folder)
        self.scanButton.clicked.connect(self.start_scan)
        self.pauseButton.clicked.connect(self.pause_scan)

        # Initialize scan-related variables
        self.scan_thread = None
        self.scan_paused = False
        self.selected_path = ""

    def select_folder(self):
        """Opens a dialog to select a folder and updates the UI."""
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.selected_path = folder
            self.selectedPathLabel.setText(f"Selected Path: {folder}")
            self.log_status(f"Selected folder: {folder}")

    def start_scan(self):
        """Starts the scanning process in a separate thread."""
        if not self.selected_path:
            QMessageBox.warning(self, "Warning", "Please select a folder first!")
            return

        self.log_status("Starting scan...")
        self.scan_thread = ScanThread(self.selected_path)
        self.scan_thread.progress_signal.connect(self.update_progress)
        self.scan_thread.status_signal.connect(self.log_status)
        self.scan_thread.start()

    def pause_scan(self):
        """Pauses or resumes the scanning process."""
        if self.scan_thread and self.scan_thread.isRunning():
            self.scan_paused = not self.scan_paused
            self.scan_thread.paused = self.scan_paused
            status = "paused" if self.scan_paused else "resumed"
            self.log_status(f"Scan {status}.")

    def update_progress(self, value):
        """Updates the progress bar."""
        self.progressBar.setValue(value)

    def log_status(self, message):
        """Logs status messages to the output display."""
        self.statusOutput.append(message)

# Background Thread for Scanning
class ScanThread(QThread):
    progress_signal = pyqtSignal(int)
    status_signal = pyqtSignal(str)

    def __init__(self, root_folder):
        super().__init__()
        self.root_folder = root_folder
        self.paused = False

    def run(self):
        """Scans the selected folder recursively, finding images."""
        image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"}
        total_files = sum(len(files) for _, _, files in os.walk(self.root_folder))
        scanned_files = 0

        for root, _, files in os.walk(self.root_folder):
            for file in files:
                while self.paused:
                    self.msleep(500)  # Pause check

                scanned_files += 1
                file_path = os.path.join(root, file)
                if os.path.splitext(file)[1].lower() in image_extensions:
                    self.status_signal.emit(f"Found image: {file_path}")

                progress = int((scanned_files / total_files) * 100) if total_files > 0 else 0
                self.progress_signal.emit(progress)

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChronoPix()
    window.show()
    sys.exit(app.exec())
