from nodes import *
import os, shutil


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
    print(f"Deleting the following files in {destination}:")
    for filename in os.listdir(destination):
        print(f"\t{filename}")
    
    shutil.rmtree(destination)
    os.mkdir(destination)
    print("Copying files...")
    __copy_recursive(source, destination)


def main():
    copy_static("static", "public")


if __name__ == '__main__':
    main()