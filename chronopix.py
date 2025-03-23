from PyQt6.QtWidgets import QApplication, QMainWindow, QTreeView
from PyQt6.QtGui import QFileSystemModel  # Corrected import
from PyQt6 import uic
import sys

class ChronoPix(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("chronopix.ui", self)  # Load UI

        # Set up file system model for the tree view
        self.model = QFileSystemModel()
        self.model.setRootPath("")  # Show entire filesystem
        self.volumeTreeView.setModel(self.model)
        self.volumeTreeView.setRootIndex(self.model.index("/"))  # Default root is system root "/"

        # Handle scan button click
        self.scanButton.clicked.connect(self.start_scan)

    def start_scan(self):
        """Example function to display selected path"""
        index = self.volumeTreeView.currentIndex()
        if index.isValid():
            path = self.model.filePath(index)
            self.infoText.append(f"Scanning: {path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChronoPix()
    window.show()
    sys.exit(app.exec())
