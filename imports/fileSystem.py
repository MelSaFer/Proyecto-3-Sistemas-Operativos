from imports.directory import Directory
from imports.file import File
from datetime import datetime
import re
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
        print("Free sectors:", self.disk.free_sectors)
        print("FAT:", self.disk.fat)

        valid_name = use_regex(name)
        if not valid_name:
            raise ValueError("Name of file is missing extension or contains invalid characters.")
        if name in self.current_directory.children:
            return None
        
        new_file = File(name, content, size, self.current_directory)

        # Allocate file
        result = self.allocateFile(new_file)
        if not result:
            return False
        self.current_directory.add_item(new_file)
        return True
    
    # Method for modifying a file
    def modify_item(self, name, content):
        if name in self.current_directory.children:
            item = self.current_directory.get_item(name)
            if isinstance(item, File):
                allocated = self.allocateNewSectors(name, content)
                if not allocated:
                    raise ValueError("Not enough disk space available")
                item.modify_content(content)
                item.modification_time = datetime.now()
                item.size = len(content)
                self.current_directory.children[name] = item
            else:
                raise ValueError("Directories can not be modified.")
        else:
            raise ValueError(f"No item named {name} found in {self.current_directory.path}")

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
        elif path == "root":
            self.current_directory = self.root
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
            self.deallocateFile(name)
        else:
            raise ValueError("Item not found!")

        
    ''' ----------------------------------- 
        Methods for file allocation

        This method allocates a file in the
        virtual disk using the FAT table
        for linked allocation
        ----------------------------------- '''
    def allocateFile(self, new_file):
        # Get the size of the file
        file_size = new_file.size

        # Get the number of sectors needed
        sectors_needed = self.get_sectors_needed(file_size)

        # Check if there is enough space in the disk
        if sectors_needed > self.disk.free_sector_count():
            return False
            raise ValueError("Not enough disk space available")
            
        # Find the first free sector
        first_sector = self.disk.find_free_sector()
        if first_sector is None:
            return False
            raise ValueError("No disk space available")
        
        # Allocate the first sector
        self.disk.write_sector(first_sector, new_file.content[:self.disk.sector_size])

        # Update the FAT table
        self.disk.fat[new_file.name] = [first_sector]

        print("ALLOCATE Free sectors:", self.disk.free_sectors)
        print("FAT:", self.disk.fat)

        sectors_needed -= 1

        # Allocate the rest of the sectors
        for i in range(0, sectors_needed):
            next_sector = self.disk.find_free_sector()
            if next_sector is None:
                return False
                raise ValueError("Not enough disk space available")
            self.disk.write_sector(next_sector, new_file.content[i*self.disk.sector_size:(i+1)*self.disk.sector_size])
            self.disk.fat[new_file.name] += [next_sector]
            
        print("free sectors:", self.disk.free_sectors)
        print("fat:", self.disk.fat)

        return True
    
    '''
    -----------------------------------
    Method for allocating new sectors
    args: file_name, new_content
    returns: True if the sectors were allocated
             False if the sectors were not allocated
    -----------------------------------
    '''
    def allocateNewSectors(self, file_name, new_content):
        # Get the size of the file
        file_size = len(new_content)

        # Get the number of sectors needed
        sectors_needed = self.get_sectors_needed(file_size)

        # Check if needs to add or remove sectors
        result = self.add_or_remove(sectors_needed, len(self.disk.fat[file_name]))

        if result == 1:
            # Check if there is enough space in the disk
            if not self.validate_space(file_size, len(self.disk.fat[file_name])):
                return False
                raise ValueError("Not enough disk space available")
        
            lastSector = self.disk.fat[file_name][-1]

            # Allocate the rest of the sectors
            for i in range(lastSector, sectors_needed - 1):
                next_sector = self.disk.find_free_sector()
                if next_sector is None:
                    return False
                    raise ValueError("Not enough disk space available")
                self.disk.write_sector(next_sector, new_content[i*self.disk.sector_size:(i+1)*self.disk.sector_size])
                self.disk.fat[file_name] += [next_sector]
        else:
            # Deallocate sectors
            for i in range(sectors_needed, len(self.disk.fat[file_name])):
                self.disk.free_sectors[self.disk.fat[file_name][i]] = True
            self.disk.fat[file_name] = self.disk.fat[file_name][:sectors_needed]

            # Replace the content of the file
            for i in range(0, sectors_needed):
                self.disk.write_sector(self.disk.fat[file_name][i], new_content[i*self.disk.sector_size:(i+1)*self.disk.sector_size])
            
        print("free sectors:", self.disk.free_sectors)
        print("fat:", self.disk.fat)

        return True


    '''
    -----------------------------------
    Method for validating the space in the disk
    args: file_size, sectors
    returns: True if there is enough space
             False if there is not enough space
    -----------------------------------
    '''
    def validate_space(self, file_size, sectors):
        # Get the number of sectors needed
        sectors_needed = file_size // self.disk.sector_size
        if file_size % self.disk.sector_size != 0:
            sectors_needed += 1

        print("Sectors needed:", sectors_needed)
        print("Sectors:", sectors)
        print("Free sectors:", self.disk.free_sector_count())

        # Check if there is enough space in the disk
        if sectors_needed > sectors:
            if sectors_needed - sectors > self.disk.free_sector_count():
                return False
        return True
    
    '''
    -----------------------------------
    Method for adding or removing sectors
    args: sectors_needed, sectors
    returns: 1 if sectors_needed > sectors
             2 if sectors_needed <= sectors
    -----------------------------------
    '''
    def add_or_remove(self, sectors_needed, sectors):
        if sectors_needed > sectors:
            return 1
        return 2


    '''
    -----------------------------------
    Method for getting the number of sectors needed
    args: file_size
    returns: sectors_needed
    --------------------------------
    '''
    def get_sectors_needed(self, file_size):
        # Get the number of sectors needed
        sectors_needed = file_size // self.disk.sector_size
        if file_size % self.disk.sector_size != 0:
            sectors_needed += 1
        return sectors_needed


    ''' 
    -----------------------------------
    Method for file deallocation
    ----------------------------------- 
    '''
    def deallocateFile(self, file_name):
        # Validate the file name
        if file_name not in self.disk.fat:
            raise ValueError("File not found.")
        
        # Get the sectors of the file
        sectors = self.disk.fat[file_name]

        # Free the sectors
        for sector in sectors:
            self.disk.free_sectors[sector] = True

        # Remove the file from the FAT table
        del self.disk.fat[file_name]

        print("DEALLOCATE Free sectors:", self.disk.free_sectors)
        print("FAT:", self.disk.fat)

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

        if name[0] == ".":
            return self.findByExtension(name)

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
    

    def findByExtension(self, extension: str):
        matches = []
        elements = [(self.root, self.root.name)]

        while elements:
            current_directory, current_path = elements.pop()

            for item in current_directory.children.values():
                path = f"{current_path}/{item.name}"
                if isinstance(item, File):
                    if item.extension == extension:
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

def use_regex(input_text):
    pattern = re.compile(r"[A-Za-z0-9\.]+\.[A-Za-z]+", re.IGNORECASE)
    return pattern.match(input_text)