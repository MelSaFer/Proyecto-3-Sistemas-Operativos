from imports.fileSystemItem import FileSystemItem


class File(FileSystemItem):
    def __init__(self, name, content, parent=None):
        super().__init__(name, parent)
        self.content = content