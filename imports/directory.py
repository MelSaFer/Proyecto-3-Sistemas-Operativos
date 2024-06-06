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

    def remove_item(self, name):
        if name in self.children:
            del self.children[name]
        else:
            raise KeyError(f"No item named {name} found in {self.path}")

    def list_items(self):
        return [(name, 'Directory' if isinstance(item, Directory) else 'File') for name, item in self.children.items()]