from imports.directory import Directory
from imports.file import File


# FileSystem Class
class FileSystem:

    # Constructor
    def __init__(self):
        self.root = Directory("root")
        self.current_directory = self.root

    # Method for creating a file
    def create_file(self, name, content):
        new_file = File(name, content, self.current_directory)
        self.current_directory.add_item(new_file)

    # Method for creating a directory
    def create_directory(self, name):
        new_directory = Directory(name, self.current_directory)
        self.current_directory.add_item(new_directory)

    # Method for changing the current directory
    def change_directory(self, path):
        if path == "..":
            if self.current_directory.parent is not None:
                self.current_directory = self.current_directory.parent
            return
        elif path in self.current_directory.children:
            self.current_directory = self.current_directory.get_item(path)
        else:
            raise ValueError("Directory not found!")

    # Method for listing the contents of the current directory
    def list_directory(self):
        return self.current_directory.list_items()

    # Method for getting the content of a file
    def get_file_content(self, file_name):
        file = self.current_directory.get_item(file_name)
        if isinstance(file, File):
            return file.content
        else:
            raise ValueError("The specified name does not refer to a file")

    # Method for removing an item from the current directory
    def remove_item(self, name):
        if name in self.current_directory.children:
            del self.current_directory.children[name]
        else:
            raise ValueError("Item not found!")
