from imports.fileSystemItem import FileSystemItem
from imports.file import File

class Directory(FileSystemItem):
    def __init__(self, name, parent=None):
        super().__init__(name, parent)
        self.children = {} # dictionary to store the children of the directory

    def add_item(self, item):
        if item.name in self.children:
            raise ValueError("Item already exists!")
        self.children[item.name] = item

    def modify_item(self, name: str):
        if name in self.children:
            item = self.children[name]
            if isinstance(item, Directory):
                print("Directories can not be modified.")
                # raise ValueError("Directories can not be modified.")
            elif isinstance(item, File):
                new_content = input("Enter new content: ")
                item.modify_content(new_content)
                self.children[name] = item
        else:
            # raise KeyError(f"No item named {name} found in {self.path}")
            print(f"No item named {name} found in {self.path}")

    def get_item(self, name):
        return self.children.get(name)
    
    def view_properties(self, name: str):
        if name in self.children:
            item = self.children[name]
            print(f"Name: {item.name}")
            print(f"Creation Time: {item.creation_time}")
            print(f"Modification Time: {item.modification_time}")
            if isinstance(item, File):
                print(f"Size: {item.size}")
        else:
            # raise KeyError(f"No item named {name} found in {self.path}")
            print(f"No item named {name} found in {self.path}")

    def remove_item(self, name):
        if name in self.children:
            del self.children[name]
        else:
            raise KeyError(f"No item named {name} found in {self.path}")

    def list_items(self):
        return [(name, 'Directory' if isinstance(item, Directory) else 'File') for name, item in self.children.items()]