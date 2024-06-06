from imports.fileSystemItem import FileSystemItem


class Directory(FileSystemItem):
    def __init__(self, name, parent=None):
        super().__init__(name, parent)
        self.children = {} # dictionary to store the children of the directory

    def add_item(self, item):
        if item.name in self.children:
            raise ValueError("Item already exists!")
        self.children[item.name] = item

    def get_item(self, name):
        return self.children.get(name)

    def list_items(self):
        return self.children.keys()