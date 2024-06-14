from imports.fileSystemItem import FileSystemItem
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
CLASS: File
ATTRIBUTES:
    fileCount: int
    extension: str
    content: str
    size: int
    id: int
METHODS:
    __init__(self, name, content, size, parent=None)
    modify_content(self, new_content)
-----------------------------------------------
'''

class File(FileSystemItem):
    fileCount = 0

    def __init__(self, name, content, size, parent=None):
        super().__init__(name, parent)
        self.extension = name[name.rfind("."):] 
        self.content = content
        self.size = size
        self.id = File.fileCount
        File.fileCount += 1
        print("File created: ", self.name, self.extension, self.size, self.content)

    def modify_content(self, new_content):
        self.content = new_content
        self.modification_time = datetime.now()