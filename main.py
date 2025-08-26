import sys
import qdarktheme
import shutil
import re
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
        
    def cleanFilename(self, name: str) -> str:
        return re.sub(r"\s*\(\d\)$", "", name)

    def sortFiles(self):
        path = Path.home() / "Downloads"
        
        osuFolder = path / "osu"
        replayFolder = osuFolder / "Replay"
        skinFolder = osuFolder / "Skin"
        songFolder = osuFolder / "Song"
        
        videoFolder = path / "Video"
        docsFolder = path / "Documents"
        zipFolder = path / "Zips"
        
        replayFolder.mkdir(parents=True, exist_ok=True)
        skinFolder.mkdir(parents=True, exist_ok=True)
        songFolder.mkdir(parents=True, exist_ok=True)
        
        videoFolder.mkdir(parents=True, exist_ok=True)
        docsFolder.mkdir(parents=True, exist_ok=True)
        zipFolder.mkdir(parents=True, exist_ok=True)
        
        for item in path.iterdir():
            if item.is_file():
                if item.suffix.lower() == ".osr": #replay files
                    target = replayFolder
                    cleanName = self.cleanFilename(item.stem) + item.suffix
                    dest = target / cleanName
                    
                    if dest.exists(): #if the non duplicate version already exists
                        item.unlink
                        self.logArea.append(f"Deleted duplicate {item.name}, kept {cleanName}")
                    else: #if there is no non-duplicate versiom
                        shutil.move(str(item), dest)
                        if cleanName != item.name:
                            self.logArea.append(f"Renamed {item.name} -> {cleanName} and moved to Replay")
                        else:
                            self.logArea.append(f"Moved {cleanName} -> Replay")
                            
                elif item.suffix.lower() == ".osk": #skin files
                    target = skinFolder
                    cleanName = self.cleanFilename(item.stem) + item.suffix
                    dest = target / cleanName
                    
                    if dest.exists(): #if non duplicate exists
                        item.unlink
                        self.logArea.append(f"Deleted duplicate {item.name}, kept {cleanName}")
                    else: #if only ducplicates exist
                        shutil.move(str(item), dest)
                        if cleanName != item.name:
                            self.logArea.append(f"Renamed {item.name} -> {cleanName} and moved to Skin")
                        else:
                            self.logArea.append(f"Moved {cleanName} -> Skin")
                elif item.suffix.lower() == ".osz": #song files
                    target = songFolder
                    cleanName = self.cleanFilename(item.stem) + item.suffix
                    dest = target / cleanName
                    
                    if dest.exists(): #if original exists
                        item.unlink
                        self.logArea.append(f"Deleted duplicate {item.name}, kept {cleanName}")
                    else: #only duplicates exist
                        shutil.move(str(item), dest)
                        if cleanName != item.name:
                            self.logArea.append(f"Renamed {item.name} -> {cleanName} and moved to Song")
                        else:
                            self.logArea.append(f"Moved {cleanName} -> Song")
                elif item.suffix.lower() in [".mov", ".mp4"]: #video files
                    target = videoFolder
                    cleanName = self.cleanFilename(item.stem) + item.suffix
                    dest = target /cleanName
                    
                    if dest.exists():
                        item.unlink
                        self.logArea.append(f"Deleted duplicate {item.name}, kept {cleanName}")
                    else:
                        shutil.move(str(item), dest)
                        if cleanName != item.name:
                            self.logArea.append(f"Renamed {item.name} -> {cleanName} and moved to Video")
                        else:
                            self.logArea.append(f"Moved {cleanName} -> Video")
                elif item.suffix.lower() in [".pdf", ".md"]: #document files
                    target = docsFolder
                    cleanName = self.cleanFilename(item.stem) + item.suffix
                    dest = target / cleanName
                    
                    if dest.exists():
                        item.unlink
                        self.logArea.append(f"Deleted duplicate {item.name}, kept {cleanName}")
                    else:
                        shutil.move(str(item), dest)
                        if cleanName != item.name:
                            self.logArea.append(f"Renamed {item.name} -> {cleanName} and moved to Documents")
                        else:
                            self.logArea.append(f"Moved {cleanName} -> Documents")
                elif item.suffix.lower() == ".zip":
                    target = zipFolder
                    cleanName = self.cleanFilename(item.stem) + item.suffix
                    dest = target / cleanName
                    
                    if dest.exists():
                        item.unlink
                        self.logArea.append(f"Deleted duplicate {item.name}, kept {cleanName}")
                    else:
                        shutil.move(str(item), dest)
                        if cleanName != item.name:
                            self.logArea.append(f"Renamed {item.name} -> {cleanName} and moved to Zip")
                        else:
                            self.logArea.append(f"Moved {cleanName} -> Zip")
        
        self.file_list.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    darkStylesheet = qdarktheme.load_stylesheet()
    app.setStyleSheet(darkStylesheet)
    
    window = FileOrganizer()
    window.show()
    sys.exit(app.exec())