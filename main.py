import sys
import qdarktheme
import shutil
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QListWidget, QPushButton, QTextEdit

class FileOrganizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Organizer")
        self.setGeometry(100, 100, 900, 500)
        
        layout = QVBoxLayout()
        self.file_list = QListWidget()
        
        self.sortButton = QPushButton("Sort Files")
        self.sortButton.clicked.connect(self.sortFiles)
        layout.addWidget(self.sortButton)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        self.logArea = QTextEdit()
        self.logArea.setReadOnly(True)
        layout.addWidget(self.logArea)

    def sortFiles(self):
        path = Path.home() / "Downloads"
        
        osuFolder = path / "osu"
        replayFolder = osuFolder / "Replay"
        skinFolder = osuFolder / "Skin"
        songFolder = osuFolder / "Song"
        
        videoFolder = path / "Video"
        
        replayFolder.mkdir(parents=True, exist_ok=True)
        skinFolder.mkdir(parents=True, exist_ok=True)
        songFolder.mkdir(parents=True, exist_ok=True)
        
        videoFolder.mkdir(parents=True, exist_ok=True)
        
        for item in path.iterdir():
            if item.is_file():
                if item.suffix.lower() == ".osr": #replay files
                    shutil.move(str(item), replayFolder / item.name)
                    self.logArea.append(f"Moved {item.name} -> Replay")
                elif item.suffix.lower() == ".osk": #skin files
                    shutil.move(str(item), skinFolder / item.name)
                    self.logArea.append(f"Moved {item.name} -> Skin")
                elif item.suffix.lower() == ".osz": #song files
                    shutil.move(str(item), songFolder / item.name)
                    self.logArea.append(f"Moved {item.name} -> Song")
                elif item.suffix.lower() in [".mov", ".mp4"]:
                    shutil.move(str(item), videoFolder / item.name)
                    self.logArea.append(f"Moved {item.name} -> Video")
        
        self.file_list.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    darkStylesheet = qdarktheme.load_stylesheet()
    app.setStyleSheet(darkStylesheet)
    
    window = FileOrganizer()
    window.show()
    sys.exit(app.exec())