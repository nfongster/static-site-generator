from nodes import *
from conversion import *
import os, shutil, sys


def __copy_recursive(source, destination):
    if os.path.isfile(source):
        print(f"Copying {source} ---> {destination}")
        shutil.copy(source, destination)
        return
    
    print(f"Recursively copying files in {source} ---> {destination}")
    if not os.path.exists(destination):
        os.mkdir(destination)
    for item in os.listdir(source):
        __copy_recursive(os.path.join(source, item), os.path.join(destination, item))


def copy_static(source, destination):
    if not os.path.exists(source):
        raise ValueError(f"Nonexistent source directory: {source}")
    if not os.path.exists(destination):
        os.mkdir(destination)
    
    print(f"This app will copy the contents of {source} ---> {destination}")
    print(f"Deleting the following files/folders in {destination}:")
    for filename in os.listdir(destination):
        print(f"\t{filename}")
    
    shutil.rmtree(destination)
    os.mkdir(destination)
    print("Copying files...")
    __copy_recursive(source, destination)


def main():
    args, basepath = sys.argv, ""
    if len(args) < 2:
        print("Basepath defaulting to \"\\\".")
        basepath = "\\"
    else:
        basepath = args[1]
        print(f"Basepath: {basepath}")
    
    copy_static("static", "public")
    generate_pages_recursive("content", "template.html", "public")


if __name__ == '__main__':
    main()