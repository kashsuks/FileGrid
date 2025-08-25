import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QListWidget
import qdarktheme

class FileOrganizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Organizer")
        self.setGeometry(100, 100, 900, 500)
        
        layout = QVBoxLayout()
        self.file_list = QListWidget()
        layout.addWidget(self.file_list)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        self.loadDownloads()
    
    def loadDownloads(self):
        path = Path.home() / "Downloads"
        if path.exists():
            for item in path.iterdir():
                self.file_list.addItem(str(item.name))
        else:
            self.file_list.addItem("Downloads folder not found!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    darkStylesheet = qdarktheme.load_stylesheet()
    app.setStyleSheet(darkStylesheet)
    
    window = FileOrganizer()
    window.show()
    sys.exit(app.exec())