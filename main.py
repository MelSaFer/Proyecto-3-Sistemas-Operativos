from imports.fileSystem import FileSystem

def main():
    fs = FileSystem()

    # Crear algunos directorios
    print("Creando directorios...")
    fs.create_directory("dir1")
    fs.create_directory("dir2")
    print("Directorios creados:", fs.list_directory())

    # Cambiar al directorio 'dir1' y crear un archivo
    print("\nCambiando a dir1 y creando archivos...")
    fs.change_directory("dir1")
    fs.create_file("file1.txt", "Contenido del archivo 1")
    fs.create_file("file2.txt", "Contenido del archivo 2")
    print("Contenidos de dir1:", fs.list_directory())

    # Listar archivos en 'dir1'
    print("\nListado de archivos en dir1:")
    print(fs.list_directory())

    # Leer contenido de 'file1.txt'
    print("\nContenido de file1.txt:")
    print(fs.get_file_content("file1.txt"))

    # Regresar al directorio raíz y listar su contenido
    print("\nRegresando al directorio raíz y listando su contenido...")
    fs.change_directory("..")
    print(fs.list_directory())

    # Eliminar 'dir2'
    print("\nEliminando dir2...")
    fs.remove_item("dir2")
    print("Contenido del directorio raíz después de eliminar dir2:")
    print(fs.list_directory())

if __name__ == "__main__":
    main()
