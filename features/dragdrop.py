from PyQt6.QtWidgets import QListWidget
from PyQt6.QtCore import Qt
from pathlib import Path
import shutil

class DragDropList(QListWidget):
    def __init__(self, logArea, folders):
        super().__init__()
        self.setAcceptDrops(True)
        self.setDragEnabled(False)
        self.logArea = logArea
        self.folders = folders

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                path = Path(url.toLocalFile())
                if path.exists():
                    self.addItem(str(path.name))  # show filename in list
                    self.logArea.append(f"Dropped: {path.name}")

                    # auto move to correct folder
                    moved = False
                    for folderName, (folderPath, extensions) in self.folders.items():
                        if path.suffix.lower() in extensions:
                            folderPath.mkdir(parents=True, exist_ok=True)
                            dest = folderPath / path.name
                            shutil.move(str(path), dest)
                            self.logArea.append(f"Moved {path.name} -> {folderPath}")
                            moved = True
                            break

                    if not moved:
                        self.logArea.append(f"No matching folder for {path.name}")