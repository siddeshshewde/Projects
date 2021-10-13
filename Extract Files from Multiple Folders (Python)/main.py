import os
import shutil

def main():

    currentFolder = os.getcwd()    

    # Getting sub folder list
    subfolders = [f.path for f in os.scandir(currentFolder) if f.is_dir()]

    # Setting Destination Folder
    destinationFolder = currentFolder + "\All Files"
    print(destinationFolder)

    # Creating a destination folder (if it does not exist)
    if not os.path.exists(destinationFolder):
        os.mkdir(destinationFolder)

    # Traversing and Moving all the files to Destination Folder
    for subfolder in subfolders:
        for file in os.listdir(subfolder):
            source = os.path.join(subfolder, file)
            destination = os.path.join(destinationFolder, file)
            shutil.move(source, destination)

main()