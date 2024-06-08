from imports.directory import Directory
from imports.file import File
from imports.virtualDisk import VirtualDisk

# FileSystem Class
class FileSystem:

    # Constructor
    def __init__(self, disk: VirtualDisk):
        self.disk = disk
        self.root = Directory("root")
        self.current_directory = self.root

    # Method for creating a file
    def create_file(self, name, content, size):
        new_file = File(name, content, size, self.current_directory)
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
        
    def allocateFile(self):
        
        return
    
    # Method to print the entire file system
    def print_file_system(self):
        def recursive_print(directory: Directory, prefix=""):
            items = list(directory.children.values())
            for i, item in enumerate(items):
                is_last = (i == len(items) - 1)
                connector = "└── " if is_last else "├── "
                if isinstance(item, File):
                    print(f"{prefix}{connector}{item.name} (File)")
                elif isinstance(item, Directory):
                    print(f"{prefix}{connector}{item.name} (Directory)")
                    new_prefix = f"{prefix}{'    ' if is_last else '│   '}"
                    recursive_print(item, new_prefix)
        
        print("\n--------------------")
        print(f"{self.root.name} (Directory)")
        recursive_print(self.root)
        print("--------------------")

    # Method to find a file or directory in the file system
    # Returns the route to the file or directory, or None if it is not found
    def find(self, name: str):
        matches = []
        elements = [(self.root, self.root.name)]

        while elements:
            current_directory, current_path = elements.pop()

            for item in current_directory.children.values():
                path = f"{current_path}/{item.name}"
                if item.name == name:
                    matches.append(path)
                if isinstance(item, Directory):
                    elements.append((item, path))
        
        for match in matches:
            print(match)

        return matches
    
    # def move_item(self, name: str, path: str):
    #     item = self.current_directory.get_item(name)
    #     if not item:
    #         # raise ValueError(f"No item named {name} found in {self.current_directory.path}")
    #         print(f"No item named {name} found in {self.current_directory.path}")
    #     # if isinstance(item, Directory):
    #     #     # raise ValueError("Directories can not be moved.")
    #     #     print("Directories can not be moved.")
    #     else:
    #         new_directory = self.find(path)[0]
    #         print("length", len(new_directory))
    #         if not new_directory:
    #             # raise ValueError(f"No directory found at {path}")
    #             print(f"No directory found at {path}")
    #         if new_directory == self.current_directory:
    #             new_name = input("Enter the new name for the file: ")
    #             item.name = new_name
    #         new_directory.add_item(item)
    #         self.current_directory.remove_item(name)

    def move_item(self, name, new_path):
        item = self.current_directory.get_item(name)

        if item is None:
            print(f"No item named {name} found in {self.current_directory.path}")
            return
        
        new_parent = self.get_directory(new_path)

        if new_parent is None:
            print(f"No directory found at {new_path}")
            return
        
        if new_parent is self.current_directory:
            new_name = input("Enter the new name for the file: ")
            item.name = new_name

        del self.current_directory.children[name]
        item.parent = new_parent
        new_parent.add_item(item)

        print(f"Item {name} moved to {new_path}")

    # Method to get a directory given its path without the root
    def get_directory(self, path):
        if path == "" or path == "root":
            return self.root
        components = path.split("/")
        
        # print(components)
        directory = self.root

        for component in components:
            print("directorio actual: ", directory.name)
            if component == "..":
                if directory.parent is not None:
                    directory = directory.parent
            elif component == "":
                continue
            else:
                next_directory = directory.get_item(component)
                if not isinstance(next_directory, Directory):
                    print(f"No directory named {component} found in {directory.path}")
                    return None
                directory = next_directory
        print(directory.name)
        return directory
