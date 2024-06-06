from datetime import datetime



class FileSystemItem:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.creation_time = datetime.now()
        self.modification_time = datetime.now()
        self.path = self.compute_path() # calculate the path of the file

        
    def compute_path(self):
        if self.parent:
            return f"{self.parent.path}/{self.name}"
        return self.name