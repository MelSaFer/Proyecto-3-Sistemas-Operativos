import tkinter as tk
from tkinter import messagebox, simpledialog
from imports.fileSystem import FileSystem
from imports.directory import Directory
from imports.file import File
from imports.virtualDisk import VirtualDisk


# FUNTIONS FOR CREATE FILE SYSTEM
'''---------------------------------------------------------------------------
Function to create a file system with the given disk size and sector count
Entries: diskSize - the size of the disk in bytes
            sectorCount - the quantity of sectors
Returns: True if the file system was created successfully, False otherwise
---------------------------------------------------------------------------'''
def createFileSystem(diskSize, sectorCount, sectors, parentWindow):
    try:
        global fs, isFileSystemCreated
        virtualDisk = VirtualDisk("virtual_disk.bin", diskSize, sectorCount, sectors)
        fs = FileSystem(virtualDisk)
        messagebox.showinfo("Success", "File system created successfully!", parent=parentWindow)
        isFileSystemCreated = True
        parentWindow.destroy()
        updateRootWindow()
    except Exception as e:
        messagebox.showerror("Error", str(e), parent=parentWindow)

'''---------------------------------------------------------------------------
Function to submit the disk size and sector count to create a file system
Entries: diskSizeEntry - the entry widget for the disk size
            sectorCountEntry - the entry widget for the sector count
            window - the window to close after the submission
---------------------------------------------------------------------------'''
def submitDiskInfo(diskSizeEntry, sectorCountEntry, window):
    try:
        diskSize = int(diskSizeEntry.get())
        sectorCount = int(sectorCountEntry.get())
        if diskSize % sectorCount != 0:
            messagebox.showerror("Error", "The size of the disk must be a multiple of the sector size.", parent=window)
        else:
            createFileSystem(diskSize, diskSize//sectorCount, sectorCount, window)
    except ValueError:
        messagebox.showerror("Error", "Please enter valid integers for disk size and sector quantity.", parent=window)


'''---------------------------------------------------------------------------
Function to create a window to input the disk size and sector count
Entries: none
Returns: none
---------------------------------------------------------------------------'''
def createFileSystemWindow():

    if isFileSystemCreated:
        response = messagebox.askyesno("Warning", "A file system has already been created. Creating a new file system will overwrite the existing one. Do you want to continue?")
        if not response:
            return
        
    root.withdraw()
    diskInputWindow = tk.Tk()
    diskInputWindow.title("Virtual Disk Setup")
    diskInputWindow.geometry("400x150")
    # center the window
    diskInputWindow.eval('tk::PlaceWindow . center')
    diskInputWindow.protocol("WM_DELETE_WINDOW", exitProgram)

    tk.Label(diskInputWindow, text="Enter the size of the virtual disk in bytes:").grid(row=0, column=0, padx=10, pady=10)
    diskSizeEntry = tk.Entry(diskInputWindow)
    diskSizeEntry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(diskInputWindow, text="Enter the quantity of sectors:").grid(row=1, column=0, padx=10, pady=10)
    sectorCountEntry = tk.Entry(diskInputWindow)
    sectorCountEntry.grid(row=1, column=1, padx=10, pady=10)

    submitButton = tk.Button(diskInputWindow, text="Create", command=lambda: submitDiskInfo(diskSizeEntry, sectorCountEntry, diskInputWindow))
    submitButton.grid(row=2, columnspan=2, pady=10)


'''---------------------------------------------------------------------------
Function to submit the file name and content to create a file
Entries: fileNameEntry - the entry widget for the file name
            fileContentEntry - the entry widget for the file content
            window - the window to close after the submission
---------------------------------------------------------------------------'''
def submitFile(fileNameEntry, fileContentEntry, window):
    try:
        fileName = fileNameEntry.get()
        fileContent = fileContentEntry.get()
        isCreated = fs.create_file(fileName, fileContent, len(fileContent))
        if isCreated == None: # The file exists. Asks user if wants to overwrite it
            response = messagebox.askyesno("Warning", "A file with the same name already exists. Do you want to overwrite it?")
            if not response:
                return
            
            # Remove the file 
            auxFile = fs.current_directory.get_item(fileName)
            fs.remove_item(fileName)

            # Create the file 
            isCreated = fs.create_file(fileName, fileContent, len(fileContent))
            if not isCreated: # The file could not be created
                print("creating file again...")
                fs.create_file(auxFile.name, auxFile.content, len(auxFile.content))
                raise ValueError("The file could not be created.")
        if not isCreated:
            raise ValueError("The file could not be created.")

        messagebox.showinfo("Success", "File created successfully!", parent=window)
        window.destroy()
        root.deiconify()
        updateRootWindowItems()
    except ValueError as e:
        messagebox.showerror("Error", str(e), parent=window)

'''---------------------------------------------------------------------------
Function to create a file
Entries: none
Returns: none
---------------------------------------------------------------------------'''  
def createFile():
    root.withdraw()
    diskInputWindow = tk.Tk()
    diskInputWindow.title("Create File")
    diskInputWindow.geometry("570x340")
    # center the window
    diskInputWindow.eval('tk::PlaceWindow . center')
    diskInputWindow.protocol("WM_DELETE_WINDOW", exitProgram)

    tk.Label(diskInputWindow, text="Enter the name of the file:").grid(row=0, column=0, padx=10, pady=10)
    fileNameEntry = tk.Entry(diskInputWindow)
    fileNameEntry.grid(row=0, column=1, padx=40, pady=10, ipadx=100)

    tk.Label(diskInputWindow, text="Enter the content of the file:").grid(row=1, column=0, padx=10, pady=10)
    fileContentEntry = tk.Entry(diskInputWindow)
    fileContentEntry.grid(row=1, column=1, padx=40, ipady=100, ipadx=100)

    cancelButton = tk.Button(diskInputWindow, text="Cancel", command=lambda: closeWindow(diskInputWindow, root))
    submitButton = tk.Button(diskInputWindow, text="Create", command=lambda: submitFile(fileNameEntry, fileContentEntry, diskInputWindow))

    #center the buttons
    cancelButton.grid(row=2, column=0, pady=10)
    submitButton.grid(row=2, column=1, pady=10)


'''---------------------------------------------------------------------------
Function to submit the modified file name and content
Entries: fileNameEntry - the entry widget for the file name
            fileContentEntry - the entry widget for the file content
            window - the window to close after the submission   
---------------------------------------------------------------------------'''
def submitModifiedFile(fileNameEntry, fileContentEntry, window):
    try:
        fileName = fileNameEntry.get()
        fileContent = fileContentEntry.get()        
        fs.modify_item(fileName, fileContent)
        messagebox.showinfo("Success", "File modified successfully!", parent=window)
        window.destroy()
        root.deiconify()
        updateRootWindowItems()
    except ValueError as e:
        messagebox.showerror("Error", str(e), parent=window)

'''---------------------------------------------------------------------------
Function to modify a file
Entries: none
Returns: none
---------------------------------------------------------------------------'''
def modifyItem():
    root.withdraw()
    diskInputWindow = tk.Tk()
    diskInputWindow.title("Modify File")
    diskInputWindow.geometry("570x340")
    # center the window
    diskInputWindow.eval('tk::PlaceWindow . center')
    diskInputWindow.protocol("WM_DELETE_WINDOW", exitProgram)

    tk.Label(diskInputWindow, text="Enter the name of the file:").grid(row=0, column=0, padx=10, pady=10)
    fileNameEntry = tk.Entry(diskInputWindow)
    fileNameEntry.grid(row=0, column=1, padx=40, pady=10, ipadx=100)

    tk.Label(diskInputWindow, text="Enter the content of the file:").grid(row=1, column=0, padx=10, pady=10)
    fileContentEntry = tk.Entry(diskInputWindow)
    fileContentEntry.grid(row=1, column=1, padx=40, ipady=100, ipadx=100)

    cancelButton = tk.Button(diskInputWindow, text="Cancel", command=lambda: closeWindow(diskInputWindow, root))
    submitButton = tk.Button(diskInputWindow, text="Modify", command=lambda: submitModifiedFile(fileNameEntry, fileContentEntry, diskInputWindow))

    #center the buttons
    cancelButton.grid(row=2, column=0, pady=10)
    submitButton.grid(row=2, column=1, pady=10)
    
'''---------------------------------------------------------------------------
Function to create a directory
Entries: none
Returns: none
---------------------------------------------------------------------------'''
def createDirectory():
    root.withdraw()
    directoryName = simpledialog.askstring("Create Directory", "Enter the name of the directory:")

    if directoryName is None:
        root.deiconify()  
        return
    try:
        fs.create_directory(directoryName)
        messagebox.showinfo("Success", "Directory created successfully!")
        # updateCurrentDirectoryLabel()
        updateRootWindowItems()
    except ValueError as e:
        messagebox.showerror("Error", str(e))
    root.deiconify()
    return

'''---------------------------------------------------------------------------
Function to change the current directory
Entries: none
Returns: none
---------------------------------------------------------------------------'''
def changeDirectory():
    root.withdraw()
    directoryPath = simpledialog.askstring("Change Directory", "Enter the path of the directory (.. for parent directory):")

    if directoryPath is None:
        root.deiconify()  
        return

    try:
        fs.change_directory(directoryPath)
        messagebox.showinfo("Success", "Changed directory to " + fs.current_directory.path)
        updateCurrentDirectoryLabel()
        updateRootWindowItems() #! delete/modify
    except ValueError as e:
        messagebox.showerror("Error", str(e))
    root.deiconify()
    return


'''---------------------------------------------------------------------------
Function to open a file
Entries: none
Returns: none
---------------------------------------------------------------------------'''
def openFile():
    root.withdraw()
    filename = simpledialog.askstring("Open File", "Enter the name of the file to open:")

    if filename is None:
        root.deiconify()  
        return
    
    print("Opening file...")
    try:
        print(filename)
        file = fs.current_directory.get_item(filename)
        if isinstance(file, File):
            fileContent = fs.get_file_content(filename)
            fileContentWindow = tk.Tk()
            fileContentWindow.title("File Content: " + file.name)
            fileContentWindow.geometry("570x340")
            # center the window
            fileContentWindow.eval('tk::PlaceWindow . center')

            # tk.Label(fileContentWindow, text="File Name: " + file.name).pack(pady=10)
            tk.Label(fileContentWindow, text="File Content:").pack(pady=10)
            fileContentLabel = tk.Label(fileContentWindow, text=fileContent, wraplength=500, justify="left")
            fileContentLabel.pack(pady=1)

        else:
            messagebox.showerror("Error", "The item is not a file.")
    except ValueError as e:
        messagebox.showerror("Error", str(e))
    root.deiconify()
    return


'''---------------------------------------------------------------------------
Function to see the properties of a file
Entries: none
Returns: none
---------------------------------------------------------------------------'''
def seeProperties():
    root.withdraw()
    file_name = simpledialog.askstring("See Properties", "Enter the name of the file to see properties:")

    if file_name is None:
        root.deiconify()  
        return
    
    try:
        file = fs.current_directory.get_item(file_name)
        if isinstance(file, File):
            properties_window = tk.Tk()
            properties_window.title("Properties")
            properties_window.geometry("300x280")
            properties_window.eval('tk::PlaceWindow . center')
            properties_window.protocol("WM_DELETE_WINDOW", exitProgram)

            tk.Label(properties_window, text="File Name: " + file.name).pack(pady=10)
            tk.Label(properties_window, text="File Extension: " + file.extension).pack(pady=10)
            tk.Label(properties_window, text="File Size: " + str(file.size) + " bytes").pack(pady=10)
            tk.Label(properties_window, text="Creation Time: " + file.creation_time.strftime("%Y-%m-%d %H:%M:%S")).pack(pady=10)
            tk.Label(properties_window, text="Modification Time: " + file.modification_time.strftime("%Y-%m-%d %H:%M:%S")).pack(pady=10)

            closeButton = tk.Button(properties_window, text="Close", command=lambda: closeWindow(properties_window, root))
            closeButton.pack(pady=10)
        else:
            raise ValueError("The specified name does not refer to a file")
    except ValueError as e:
        messagebox.showerror("Error", str(e))
    root.deiconify()
    return

'''---------------------------------------------------------------------------
Function to list the contents of the current directory
Entries: none
Returns: none
---------------------------------------------------------------------------'''
def listDirectory():
    return

'''---------------------------------------------------------------------------
Function to remove an item from the current directory
Entries: none
Returns: none
---------------------------------------------------------------------------'''
def removeItem():
    root.withdraw()
    itemName = simpledialog.askstring("Remove Item", "Enter the name of the item to remove:")

    if itemName is None:
        root.deiconify()  
        return

    if itemName is None:
        root.deiconify()  
        return
    
    try:
        fs.remove_item(itemName)
        messagebox.showinfo("Success", "Item removed successfully!")
        updateRootWindowItems()
    except ValueError as e:
        messagebox.showerror("Error", str(e))
    root.deiconify()
    return


'''---------------------------------------------------------------------------
Function to find an item in the file system
Entries: none
Returns: none
---------------------------------------------------------------------------'''
def find():
    root.withdraw()
    itemName = simpledialog.askstring("Find Item", "Enter the name of the item to find:")

    if itemName is None:
        root.deiconify()  
        return
    
    try:
        matches = fs.find(itemName)
        if len(matches) == 0:
            messagebox.showinfo("Find", "No matches found.")
        else:
            matches_window = tk.Tk()
            matches_window.title("Find Results")
            

            matches_window.geometry("300x280")
            matches_window.eval('tk::PlaceWindow . center')
            matches_window.protocol("WM_DELETE_WINDOW", exitProgram)

            tk.Label(matches_window, text="Matches for " + itemName + ":").pack(pady=10)
            for match in matches:
                tk.Label(matches_window, text=match).pack(pady=5)

            closeButton = tk.Button(matches_window, text="Close", command=lambda: closeWindow(matches_window, root))
            closeButton.pack(pady=10)
    except ValueError as e:
        messagebox.showerror("Error", str(e))
    root.deiconify()
    matches_window = tk.Toplevel(root)
    
    return

def printTree():
    root.withdraw()
    diskInputWindow = tk.Tk()
    diskInputWindow.title("TREE")
    diskInputWindow.geometry("570x340")
    # center the window
    diskInputWindow.eval('tk::PlaceWindow . center')
    def on_close():
        diskInputWindow.destroy()
        root.deiconify()

    diskInputWindow.protocol("WM_DELETE_WINDOW", on_close)

    try:
        text = tk.Text(diskInputWindow, wrap="word", padx=10, pady=10, font=("Courier New", 10))
        text.pack(expand=True, fill="both")

        # Insertar el texto del sistema de archivos en el widget Text
        text.insert(tk.END, fs.print_file_system())
        text.configure(state="disabled")  # Hacer el widget Text de solo lectura

        print(fs.print_file_system())
    except ValueError as e:
        messagebox.showerror("Error", str(e))
    # root.deiconify()
    return


def copyFileToMachine():
    root.withdraw()
    itemName = simpledialog.askstring("Copy File", "Enter the name of the file to copy:")
    if itemName is None:
        root.deiconify()  
        return
    pc_path = simpledialog.askstring("Copy File", "Enter the path where you want to copy the file:")
    if pc_path is None:
        root.deiconify()  
        return
    if itemName is None:
        root.deiconify()  
        return
    try:
        print("Item name: ", itemName)
        result = fs.copy_virtual_to_real(f'{"root" + chr(47) + itemName}', pc_path)
        if not result:
            raise ValueError("The file could not be copied.")
        messagebox.showinfo("Success", "File copied successfully!")
    except ValueError as e:
        messagebox.showerror("Error", str(e))
    root.deiconify()
    return

# GENERAL FUNCTIONS

def closeWindow(window, root):
    window.destroy()
    root.deiconify()

def exitProgram():
    # Actual command to close the application
    print("Exiting program...")
    root.quit()

def menubar(window):
    menubar = tk.Menu(window)
    
    if isFileSystemCreated:
        # menubar.add_command(label="Create File System", command=createFileSystemWindow)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Create File", command=createFile)
        file_menu.add_command(label="Remove File", command=removeItem)
        file_menu.add_command(label="Modify File", command=modifyItem)
        file_menu.add_command(label="Open File", command=openFile)
        file_menu.add_command(label="See Properties", command=seeProperties)
        file_menu.add_separator()
        # file_menu.add_command(label="Exit", command=exitProgram)
        menubar.add_cascade(label="Files", menu=file_menu)

        directory_menu = tk.Menu(menubar, tearoff=0)
        directory_menu.add_command(label="Create Directory", command=createDirectory)
        directory_menu.add_command(label="Change Directory", command=changeDirectory)
        directory_menu.add_command(label="List Directory", command=listDirectory)
        directory_menu.add_command(label="Remove Item", command=removeItem)
        menubar.add_cascade(label="Directories", menu=directory_menu)

        actions_menu = tk.Menu(menubar, tearoff=0)
        actions_menu.add_command(label="Find", command=find)
        actions_menu.add_command(label="Tree", command=printTree)
        actions_menu.add_separator()
        actions_menu.add_command(label="Copy File to Machine", command=copyFileToMachine)
        menubar.add_cascade(label="Actions", menu=actions_menu)

        menubar.add_command(label="Exit", command=exitProgram)
    else:
        menubar.add_command(label="Create File System", command=createFileSystemWindow)

    return menubar  

def updateCurrentDirectoryLabel():
    global currentDirectoryLabel
    global fs
    currentDirectoryLabel.config(text="Current Directory: " + fs.current_directory.path)


def updateRootWindow():
    global currentDirectoryLabel
    global labelFrame

    root.deiconify()
    print("Updating root window after creating file...")
    menu = menubar(root)  
    root.config(menu=menu)  # Configure the root window to use the created menu bar
    
    labelFrame = tk.Frame(root, borderwidth=2, relief="groove")
    labelFrame.pack(padx=10, pady=10, fill="x")


    currentDirectoryLabel = tk.Label(labelFrame, text="Current Directory: " + fs.current_directory.path, anchor="w")
    currentDirectoryLabel.pack(side="left", padx=10, fill="x")

# temp function to update the items in the root window 
# ! delete later
def updateRootWindowItems():
    global fs
    global currentDirectoryLabel
    #clean the window
    for widget in root.winfo_children():
        # if widget is  Label delete
        if isinstance(widget, tk.Label):
            widget.destroy()

    updateCurrentDirectoryLabel()

    items = fs.list_directory()
    for item in items:
        tk.Label(root, text=item[0] + " - " + item[1]).pack(fill="x")
        
    

def main():
    # Initialize global variables
    global root  
    global isFileSystemCreated  
    isFileSystemCreated = False  # Flag to check if a file system has been created
    root = tk.Tk()
    root.title("File System")
    root.geometry("300x200")
    root.eval('tk::PlaceWindow . center')
    root.protocol("WM_DELETE_WINDOW", exitProgram)

    # Create and set the menu bar
    menu = menubar(root) 
    root.config(menu=menu)  

    root.mainloop()

main()

# TESTING