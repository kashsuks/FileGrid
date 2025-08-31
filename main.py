import sys
import qdarktheme
import shutil
import re
import time

from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QListWidget, QPushButton, QTextEdit, QMessageBox
from features.dragdrop import DragDropList

class FileOrganizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Organizer")
        self.setGeometry(100, 100, 900, 500)

        layout = QVBoxLayout()
        self.fileList = QListWidget()

        self.sortButton = QPushButton("Sort Files")
        self.sortButton.clicked.connect(self.sortFiles)
        layout.addWidget(self.sortButton)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.logArea = QTextEdit()
        self.logArea.setReadOnly(True)
        layout.addWidget(self.logArea)

        # define folders ONCE and reuse
        downloadsPath = Path.home() / "Downloads"
        self.folders = {
            "Replay": (downloadsPath / "osu" / "Replay", [".osr"]),
            "Skin": (downloadsPath / "osu" / "Skin", [".osk"]),
            "Song": (downloadsPath / "osu" / "Song", [".osz"]),
            "Video": (downloadsPath / "Video", [".mov", ".mp4"]),
            "Documents": (downloadsPath / "Documents", [".pdf", ".md"]),
            "Zips": (downloadsPath / "Zips", [".zip"]),
            "Images": (downloadsPath / "Images", [".png", ".jpeg", ".jpg", ".heic"]),
            "Applications": (downloadsPath / "Applications", [".app", ".dmg", ".exe"]),
        }

        self.dragDropList = DragDropList(self.logArea, self.folders)
        layout.addWidget(self.dragDropList)

    def cleanFilename(self, name: str) -> str:
        return re.sub(r"\s*\(\d\)$", "", name)

    def sortFiles(self):
        daysInSeconds = 30 * 24 * 60 * 60
        downloadsPath = Path.home() / "Downloads"

        for folderPath, _ in self.folders.values():
            folderPath.mkdir(parents=True, exist_ok=True)

        for item in downloadsPath.iterdir():
            targetFolder = None
            for folderName, (folderPath, extensions) in self.folders.items():
                if (item.suffix.lower() in extensions) or (
                    item.is_dir() and ".app" in extensions and item.suffix.lower() == ".app"
                ):
                    targetFolder = folderPath
                    break

            if not targetFolder:
                continue

            cleanName = self.cleanFilename(item.stem) + item.suffix
            dest = targetFolder / cleanName

            fileAge = time.time() - item.stat().st_ctime

            if dest.exists():
                if fileAge > daysInSeconds:
                    reply = QMessageBox.question(
                        self,
                        "Old file detected",
                        f"{item.name} is over 30 days old. Do you want to delete it?",
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    )

                    if reply == QMessageBox.StandardButton.Yes:
                        if item.is_file():
                            item.unlink()
                        else:
                            shutil.rmtree(item)
                        self.logArea.append(f"Deleted old file {item.name}, kept {cleanName}")
                        continue
                    else:
                        self.logArea.append(f"Kept old file {item.name}")
                        continue

                if item.is_file():
                    item.unlink()
                else:
                    shutil.rmtree(item)
                self.logArea.append(f"Deleted duplicate {item.name}, kept {cleanName}")
            else:
                shutil.move(str(item), dest)
                if cleanName != item.name:
                    self.logArea.append(f"Renamed {item.name} -> {cleanName} and moved to {targetFolder.name}")
                else:
                    self.logArea.append(f"Moved {cleanName} -> {targetFolder.name}")

        self.fileList.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    darkStylesheet = qdarktheme.load_stylesheet()
    app.setStyleSheet(darkStylesheet)

    window = FileOrganizer()
    window.show()
    sys.exit(app.exec()) 