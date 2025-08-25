import sys
import qdarktheme
import shutil
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QListWidget, QPushButton

class FileOrganizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Organizer")
        self.setGeometry(100, 100, 900, 500)
        
        layout = QVBoxLayout()
        self.file_list = QListWidget()
        layout.addWidget(self.file_list)
        
        self.osuButton = QPushButton("Sort osu files")
        self.osuButton.clicked.connect(self.sortOsuFiles)
        layout.addWidget(self.osuButton)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def sortOsuFiles(self):
        path = Path.home() / "Downloads"
        osuFolder = path / "osu"
        replayFolder = osuFolder / "Replay"
        skinFolder = osuFolder / "Skin"
        songFolder = osuFolder / "Song"
        
        replayFolder.mkdir(parents=True, exist_ok=True)
        skinFolder.mkdir(parents=True, exist_ok=True)
        songFolder.mkdir(parents=True, exist_ok=True)
        
        for item in path.iterdir():
            if item.is_file():
                if item.suffix.lower() == ".osr": #replay files
                    shutil.move(str(item), replayFolder / item.name)
                elif item.suffix.lower() == ".osk": #skin files
                    shutil.move(str(item), skinFolder / item.name)
                elif item.suffix.lower() == ".osz":
                    shutil.move(str(item), songFolder / item.name) 
        
        self.file_list.clear()
        for item in path.iterdir():
            self.file_list.addItem(str(item.name))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    darkStylesheet = qdarktheme.load_stylesheet()
    app.setStyleSheet(darkStylesheet)
    
    window = FileOrganizer()
    window.show()
    sys.exit(app.exec())