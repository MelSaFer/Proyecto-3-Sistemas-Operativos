from imports.fileSystemItem import FileSystemItem


class File(FileSystemItem):
    def __init__(self, name, content, parent=None):
        super().__init__(name, parent)
        self.content = content

    def modify_content(self, new_content):
        self.content = new_content
        self.modification_time = datetime.now()