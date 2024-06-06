

# Vistual Disk Class
class VirtualDisk:


    def __init__(self, file_path, size):
        self.file_path = file_path
        self.size = size
        self.sector_size = 512  # Size of a sector in bytes
        self.create_virtual_disk()
        self.free_sectors = [True] * self.sectors # list of free sectors

    def create_virtual_disk(self):
        # Create the virtual disk file if it doesn't exist
        try:
            with open(self.file_path, 'r+b') as f:
                pass  # The file already exists
        except FileNotFoundError:
            with open(self.file_path, 'wb') as f:
                f.write(b'\x00' * self.size)  # Initialize the file with zeros

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
        # Read a sector from the virtual disk
        with open(self.file_path, 'rb') as f:
            f.seek(sector_index * self.sector_size)
            return f.read(self.sector_meta_size)

    def write_sector(self, sector_index, data):
        # Write a sector to the virtual disk
        with open(self.file_path, 'r+b') as f:
            f.seek(sector_index * self.sector_size)
            f.write(data.ljust(self.sector_size, b'\x00'))  # Rellena con ceros si es necesario

    def format_disk(self):
        # Format the virtual disk by writing zeros to the entire disk
        with open(self.file_path, 'r+b') as f:
            f.write(b'\x00' * self.size)

# Example of usage
# disk = VirtualDisk("virtual_disk.bin", 1024 * 1024)  # Crea un disco de 1MB
