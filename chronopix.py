import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTabWidget, QPushButton, QTreeView, QProgressBar, QLabel, 
                             QGridLayout, QStatusBar)  # Added QStatusBar here
from PyQt6.QtCore import Qt

class ChronoPixWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ChronoPix")
        self.setGeometry(100, 100, 1440, 900)
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        sidebar = QWidget()
        sidebar.setFixedWidth(300)
        sidebar_layout = QVBoxLayout(sidebar)
        self.setup_sidebar(sidebar_layout)
        main_layout.addWidget(sidebar)
        self.tabs = QTabWidget()
        self.setup_tabs()
        main_layout.addWidget(self.tabs)
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready | Scanned: 0 | Processed: 0 | Archived: 0")
        self.setStyleSheet("""
            QMainWindow { background-color: #2A2A2A; color: #FFFFFF; }
            QPushButton { background-color: #26A69A; color: #FFFFFF; }
            QTabWidget::pane { border: 1px solid #26A69A; }
        """)

    def setup_sidebar(self, layout):
        volumes_tree = QTreeView()
        layout.addWidget(QLabel("Storage Volumes"))
        layout.addWidget(volumes_tree)
        layout.addWidget(QLabel("Scan Status"))
        self.progress = QProgressBar()
        layout.addWidget(self.progress)
        filter_btn = QPushButton("Filter File Types")
        layout.addWidget(filter_btn)
        layout.addStretch()

    def setup_tabs(self):
        scan_tab = QWidget()
        scan_layout = QGridLayout(scan_tab)
        for i in range(4):
            for j in range(4):
                thumbnail = QPushButton(f"Img {i*4+j+1}")
                scan_layout.addWidget(thumbnail, i, j)
        self.tabs.addTab(scan_tab, "Scan & Detect")
        ai_tab = QWidget()
        ai_layout = QVBoxLayout(ai_tab)
        ai_layout.addWidget(QLabel("AI Categories Here"))
        self.tabs.addTab(ai_tab, "AI Analysis")
        organize_tab = QWidget()
        organize_layout = QHBoxLayout(organize_tab)
        organize_layout.addWidget(QTreeView())
        organize_layout.addWidget(QLabel("Drag images here"))
        self.tabs.addTab(organize_tab, "Organize & Backup")

    def start_scan(self):
        self.progress.setValue(50)
        self.status_bar.showMessage("Scanning... | Scanned: 123 | Processed: 50 | Archived: 0")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChronoPixWindow()
    window.show()
    sys.exit(app.exec())