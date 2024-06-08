from imports.fileSystemItem import FileSystemItem
from datetime import datetime

class File(FileSystemItem):
    def __init__(self, name, content, size, parent=None):
        super().__init__(name, parent)
        self.content = content
        self.size = size

    def modify_content(self, new_content):
        self.content = new_content
        self.modification_time = datetime.now()