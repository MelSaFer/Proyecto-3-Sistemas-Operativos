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
        fs.create_file(fileName, fileContent, len(fileContent))
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
Function to create a directory
Entries: none
Returns: none
---------------------------------------------------------------------------'''
def createDirectory():
    root.withdraw()
    directoryName = simpledialog.askstring("Create Directory", "Enter the name of the directory:")
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
    try:
        fs.remove_item(itemName)
        messagebox.showinfo("Success", "Item removed successfully!")
        updateRootWindowItems()
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
        file_menu.add_separator()
        # file_menu.add_command(label="Exit", command=exitProgram)
        menubar.add_cascade(label="Files", menu=file_menu)

        directory_menu = tk.Menu(menubar, tearoff=0)
        directory_menu.add_command(label="Create Directory", command=createDirectory)
        directory_menu.add_command(label="Change Directory", command=changeDirectory)
        directory_menu.add_command(label="List Directory", command=listDirectory)
        menubar.add_cascade(label="Directories", menu=directory_menu)

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
    #clean the window
    for widget in root.winfo_children():
        # if widget is  Label delete
        if isinstance(widget, tk.Label):
            widget.destroy()

    currentDirectoryLabel = tk.Label(labelFrame, text="Current Directory: " + fs.current_directory.path, anchor="w")
    currentDirectoryLabel.pack(side="left", padx=10, fill="x")

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