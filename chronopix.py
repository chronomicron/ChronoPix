import sys
import time
import threading
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt6.QtCore import QTimer, QDir, QThread, pyqtSignal
from PyQt6.uic import loadUi

class ScannerThread(QThread):
    """Thread to handle volume scanning."""
    progress_signal = pyqtSignal(int)  # Signal to update progress bar
    finished_signal = pyqtSignal()  # Signal when scanning is done

    def __init__(self, folder_path):
        super().__init__()
        self.folder_path = folder_path
        self.paused = False
        self.stop_scan = False

    def run(self):
        """Scans the folder and updates progress."""
        file_count = self.count_files(self.folder_path)
        scanned = 0

        for root, dirs, files in QDir(self.folder_path).entryList(QDir.Files | QDir.NoDotAndDotDot, QDir.Name):
            if self.stop_scan:
                break  # Stop scanning immediately

            while self.paused:
                time.sleep(0.1)  # Pause execution

            scanned += 1
            progress = int((scanned / file_count) * 100)
            self.progress_signal.emit(progress)
            time.sleep(0.05)  # Simulate processing time

        self.finished_signal.emit()

    def count_files(self, folder):
        """Counts all files in the directory tree for progress tracking."""
        file_count = 0
        for _, _, files in QDir(folder).entryList(QDir.Files | QDir.NoDotAndDotDot):
            file_count += len(files)
        return max(file_count, 1)  # Avoid division by zero

    def pause(self):
        """Pauses the scanning process."""
        self.paused = not self.paused  # Toggle pause state

    def stop(self):
        """Stops scanning entirely."""
        self.stop_scan = True

class ChronoPix(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("chronopix.ui", self)

        self.scanner_thread = None  # Initialize scanning thread variable

        # Connect buttons to functions
        self.scanButton.clicked.connect(self.start_scan)
        self.pauseButton.clicked.connect(self.pause_scan)
        self.selectFolderButton.clicked.connect(self.select_folder)

        self.selected_folder = None

    def select_folder(self):
        """Opens a file dialog to select a folder."""
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.selected_folder = folder

    def start_scan(self):
        """Starts scanning the selected volume."""
        if not self.selected_folder:
            print("No folder selected.")  # Later replace with a message box
            return

        self.scanner_thread = ScannerThread(self.selected_folder)
        self.scanner_thread.progress_signal.connect(self.update_progress)
        self.scanner_thread.finished_signal.connect(self.scan_complete)

        self.progressBar.setValue(0)  # Reset progress
        self.scanner_thread.start()

    def pause_scan(self):
        """Pauses the scanning process."""
        if self.scanner_thread:
            self.scanner_thread.pause()

    def update_progress(self, value):
        """Updates the progress bar."""
        self.progressBar.setValue(value)

    def scan_complete(self):
        """Handles completion of the scan."""
        print("Scanning Complete!")  # Later replace with a UI message

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChronoPix()
    window.show()
    sys.exit(app.exec())
