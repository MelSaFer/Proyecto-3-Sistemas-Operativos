from datetime import datetime
'''
-----------------------------------------------
Instituto Tecnológico de Costa Rica
Escuela de Ingeniería en Computación
Curso: Principios de Sistemas Operativos
Profesor: Erika Marín Schumman
Proyecto 3: File System
Estudiantes:
    - Salas Fernández Melany - 2021121147
    - Solano Espinoza Moisés - 2021144322
    - Zelaya Coto Fiorella - 2021453615
-----------------------------------------------
CLASS: FileSystemItem
ATTRIBUTES:
    name: str
    parent: str
    creation_time: datetime
    modification_time: datetime
METHODS:
    __init__(self, name, parent)
    compute_path(self)
-----------------------------------------------
'''
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