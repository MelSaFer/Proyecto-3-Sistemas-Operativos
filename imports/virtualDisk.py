

# Vistual Disk Class
class VirtualDisk:


    def __init__(self, file_path, size):
        self.file_path = file_path
        self.size = size
        self.sector_size = 512  # Size of a sector in bytes
        self.create_virtual_disk()
        self.free_sectors = [True] * (self.size//self.sector_size) # list of free sectors

    def create_virtual_disk(self):
        # Create the virtual disk file if it doesn't exist
        try:
            with open(self.file_path, 'r+b') as f:
                pass  # The file already exists
        except FileNotFoundError:
            with open(self.file_path, 'wb') as f:
                f.write(b'\x00' * self.size)  # Initialize the file with zeros
        #print(self.size//self.sector_size)

    def find_free_sector(self):
        # Find the first free sector in the virtual disk
        for index, is_free in enumerate(self.free_sectors):
            if is_free:
                return index
        raise Exception("No free sectors available.")
    
    def free_sector_count(self):
        # Return the number of free sectors in the virtual disk
        return sum(self.free_sectors)

    def read_sector(self, sector_index):
        with open(self.file_path, 'rb') as f:
            f.seek(sector_index * self.sector_size)
            return f.read(self.sector_size)


    def write_sector(self, sector_index, data):
        with open(self.file_path, 'r+b') as f:
            f.seek(sector_index * self.sector_size)
            f.write(data.ljust(self.sector_size, b'\x00'))  # Fill with zeros if necessary
        self.free_sectors[sector_index] = False  # Mark the sector as not free


    def format_disk(self):
        with open(self.file_path, 'r+b') as f:
            f.write(b'\x00' * self.size)
        self.free_sectors = [True] * (self.size // self.sector_size)  # Reset free sectors list


# Example of usage
#disk = VirtualDisk("virtual_disk.bin", 1024 * 1024)  # Crea un disco de 1MB
