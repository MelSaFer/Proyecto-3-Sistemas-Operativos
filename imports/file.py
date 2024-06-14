from imports.fileSystemItem import FileSystemItem
from datetime import datetime

class File(FileSystemItem):
    fileCount = 0

    def __init__(self, name, content, size, parent=None):
        super().__init__(name, parent)
        self.extension = name[name.rfind("."):] 
        self.content = content
        self.size = size
        self.id = File.fileCount
        File.fileCount += 1
        print("File created: ", self.name, self.extension, self.size, self.content)

    def modify_content(self, new_content):
        self.content = new_content
        self.modification_time = datetime.now()