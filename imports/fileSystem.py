from imports.directory import Directory
from imports.file import File


# FileSystem Class
class FileSystem:

    # Constructor
    def __init__(self, disk):
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


    # Method for recursive search of a directory
    def search_directory(self, name, directory, new_items):
        # print("Recursive search")
        # print(name + " " + directory.name + " " + str(directory.children))
        if name == directory.name:
            # print("Found 1")
            return new_items + [directory.name]
        if name in directory.children and isinstance(directory.get_item(name), Directory):
            # print("Found 2")
            return new_items + [name]
        for item_name, item in directory.children.items():
            # print(item_name + " " + str(item)) 
            result = self.search_directory(name, directory.get_item(item_name), new_items)
            if result is not None:
                return result + [item_name]
        return None

    # Method for changing the current directory
    def change_directory(self, path):
        if path == "..":
            if self.current_directory.parent is not None:
                self.current_directory = self.current_directory.parent
            return
        elif path in self.current_directory.children:
            self.current_directory = self.current_directory.get_item(path)
        else:
            items = path.split("/")
            aux_directory = self.root
            new_items = []

            for item in items:
                new_items = self.search_directory(item, aux_directory, new_items)
                if new_items == None:
                    raise ValueError("Directory not found!")
                for item in list(reversed(new_items)):
                    print(item)
                    aux_directory = aux_directory.get_item(item)
                new_items = []
            self.current_directory = aux_directory

    

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
