import sys
import qdarktheme
import shutil
import re
import time
import json

from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QPushButton,
    QHBoxLayout, QStackedWidget, QMessageBox
)
from features.dragdrop import DragDropList

CONFIG_DIR = Path.home() / ".config" / "filegrid"
CONFIG_FILE = CONFIG_DIR / "stats.json"

class FileOrganizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Organizer")
        self.setGeometry(100, 100, 900, 500)

        mainLayout = QHBoxLayout()
        self.logArea = QTextEdit()
        self.logArea.setReadOnly(True)

        downloadsPath = Path.home() / "Downloads"
        self.folders = {
            "Replay": (downloadsPath / "osu" / "Replay", [".osr"]),
            "Skin": (downloadsPath / "osu" / "Skin", [".osk"]),
            "Song": (downloadsPath / "osu" / "Song", [".osz"]),
            "Video": (downloadsPath / "Video", [".mov", ".mp4"]),
            "Documents": (downloadsPath / "Documents", [".pdf", ".md"]),
            "Zips": (downloadsPath / "Zips", [".zip"]),
            "Images": (downloadsPath / "Images", [".png", ".jpeg", ".jpg", ".heic"]),
            "Applications": (downloadsPath / "Applications", [".app", ".dmg", ".exe", ".pkg"]),
            "Code": (downloadsPath / "Code", [".py", ".go", ".cpp", ".java", ".js"]),
            "KiCad": (downloadsPath / "KiCad", [".kicad_pro", ".kicad_sch", ".kicad_pcb"]),
            "Gerbers": (downloadsPath / "KiCad" / "Gerbers", [".gbr", ".drl"]),
            "Music": (downloadsPath / "Music", [".mp3", ".wav"]),
            "Text": (downloadsPath / "Text", [".txt"]),
            "Data": (downloadsPath / "Data", [".csv", ".json"])
        }

        self.dragDropList = DragDropList(self.logArea, self.folders)

        self.homePage = QWidget()
        homeLayout = QVBoxLayout()
        homeLayout.addWidget(self.dragDropList)
        homeLayout.addWidget(self.logArea)
        self.homePage.setLayout(homeLayout)

        self.statsPage = QWidget()
        statsLayout = QVBoxLayout()
        self.statsArea = QTextEdit()
        self.statsArea.setReadOnly(True)
        statsLayout.addWidget(self.statsArea)
        self.statsPage.setLayout(statsLayout)

        self.stackedWidget = QStackedWidget()
        self.stackedWidget.addWidget(self.homePage)
        self.stackedWidget.addWidget(self.statsPage)

        # sidebar stuff
        sidebar = QVBoxLayout()
        homeButton = QPushButton("☰ Home")
        statsButton = QPushButton("Stats")
        sortButton = QPushButton("Sort Files")

        homeButton.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.homePage))
        statsButton.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.statsPage))
        sortButton.clicked.connect(self.sortFiles)

        sidebar.addWidget(homeButton)
        sidebar.addWidget(statsButton)
        sidebar.addWidget(sortButton)
        sidebar.addStretch()

        mainLayout.addLayout(sidebar)
        mainLayout.addWidget(self.stackedWidget)

        container = QWidget()
        container.setLayout(mainLayout)
        self.setCentralWidget(container)

        self.filesMoved = 0
        self.deletedSize = 0
        self.loadStats()

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
            itemSize = item.stat().st_size

            if dest.exists():
                if fileAge > daysInSeconds:
                    reply = QMessageBox.question(
                        self,
                        "Old file detected",
                        f"{item.name} is over 30 days old. Delete it?",
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    )
                    if reply == QMessageBox.StandardButton.Yes:
                        if item.is_file():
                            item.unlink()
                        else:
                            shutil.rmtree(item)
                        self.deletedSize += itemSize
                        self.logArea.append(f"Deleted old file {item.name}, kept {cleanName}")
                        self.saveStats()
                        continue
                    else:
                        self.logArea.append(f"Kept old file {item.name}")
                        continue

                if item.is_file():
                    item.unlink()
                else:
                    shutil.rmtree(item)
                self.deletedSize += itemSize
                self.logArea.append(f"Deleted duplicate {item.name}, kept {cleanName}")
                self.saveStats()
            else:
                shutil.move(str(item), dest)
                self.filesMoved += 1
                self.logArea.append(f"Moved {cleanName} -> {targetFolder.name}")
                self.saveStats()

        self.updateStats()

    def updateStats(self):
        deletedMB = self.deletedSize / (1024 * 1024)
        statsText = (
            f"Files moved: {self.filesMoved}\n"
            f"Total size of deleted files: {deletedMB:.2f} MB"
        )
        self.statsArea.setPlainText(statsText)

    def saveStats(self):
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        data = {
            "filesMoved": self.filesMoved,
            "deletedSize": self.deletedSize
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f)

    def loadStats(self):
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                self.filesMoved = data.get("filesMoved", 0)
                self.deletedSize = data.get("deletedSize", 0)
        else:
            self.filesMoved = 0
            self.deletedSize = 0
            self.saveStats()
        self.updateStats()

# driver code
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarktheme.load_stylesheet())

    window = FileOrganizer()
    window.show()
    sys.exit(app.exec())