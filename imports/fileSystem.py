from imports.directory import Directory
from imports.file import File

import re

# FileSystem Class
class FileSystem:

    # Constructor
    def __init__(self, disk):
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
            raise ValueError("File already exists!")
        
        new_file = File(name, content, size, self.current_directory)
        print("Free sectors:", self.disk.free_sectors)
        print("FAT:", self.disk.fat)

        # Allocate file
        self.allocateFile(new_file)
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
        sectors_needed = file_size // self.disk.sector_size
        if file_size % self.disk.sector_size != 0:
            sectors_needed += 1

        # Check if there is enough space in the disk
        if sectors_needed > self.disk.free_sector_count():
            raise ValueError("Not enough disk space available")
            
        # Find the first free sector
        first_sector = self.disk.find_free_sector()
        if first_sector is None:
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
                raise ValueError("No disk space available")
            self.disk.write_sector(next_sector, new_file.content[i*self.disk.sector_size:(i+1)*self.disk.sector_size])
            self.disk.fat[new_file.name] += [next_sector]
            
        print("free sectors:", self.disk.free_sectors)
        print("fat:", self.disk.fat)

        return True

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
    
def use_regex(input_text):
    pattern = re.compile(r"[A-Za-z0-9\.]+\.[A-Za-z]+", re.IGNORECASE)
    return pattern.match(input_text)
