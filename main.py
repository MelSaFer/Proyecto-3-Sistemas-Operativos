from imports.fileSystem import FileSystem
from imports.directory import Directory
from imports.file import File
from imports.virtualDisk import VirtualDisk

# Create the virtual disk globally

def Prueba(fs):

    # Crear algunos directorios
    print("Creando directorios...")
    fs.create_directory("dir1")
    fs.create_directory("dir2")
    print("Directorios creados:", fs.list_directory())

    # Cambiar al directorio 'dir1' y crear un archivo
    print("\nCambiando a dir1 y creando archivos...")
    fs.change_directory("dir1")
    fs.create_file("file1.txt", "Contenido del archivo 1", 1000	)
    fs.create_file("file2.txt", "Contenido del archivo 2", 2000)
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


def menu(fs):
    while True:
        print("\nCurrent Directory:", fs.current_directory.path)
        print("1. Create File")
        print("2. Create Directory")
        print("3. Change Directory")
        print("4. List Directory")
        print("6. Remove Item")
        print("7. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            name = input("Enter file name: ")
            content = input("Enter content of the file: ")
            try:
                fs.create_file(name, content, len(content)*1000)
                print("File created successfully.")
            except ValueError as e:
                print(e)

        elif choice == "2":
            name = input("Enter directory name: ")
            try:
                fs.create_directory(name)
                print("Directory created successfully.")
            except ValueError as e:
                print(e)

        elif choice == "3":
            path = input("Enter directory path (.. for parent directory): ")
            try:
                fs.change_directory(path)
                print("Changed directory to", fs.current_directory.path)
            except ValueError as e:
                print(e)

        elif choice == "4":
            items = fs.list_directory()
            for name, type in items:
                print(f"{name} ({type})")
            if not items:
                print("Directory is empty.")

        elif choice == "6":
            name = input("Enter the name of the item to remove: ")
            try:
                fs.current_directory.remove_item(name)
                print("Item removed successfully.")
            except KeyError as e:
                print(e)

        elif choice == "7":
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please choose a valid option.")

def main():
    #Prueba()
    virtualDisk = VirtualDisk("virtual_disk.bin", 1024 * 1024, 512)
    fs = FileSystem(virtualDisk)
    print("Virtual Disk created successfully.")
    menu(fs)

main()
