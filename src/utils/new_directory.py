from os import listdir
from os import mkdir
from os.path import join

def new_directory(dir_name, dir_location):
    """
    Create a directory if it does not exist

    dir_name: name of the target directory
    dir_location: location of the target directory

    new_dir_name: location inside the new target directory
    """
    # check if folder exists
    if dir_name in listdir(dir_location):
        print(f"Using existing folder {dir_name}/")
        return join(dir_location, dir_name)
    else:
        new_dir_name = join(dir_location, dir_name)
        mkdir(new_dir_name)
        print(f"Created new folder {dir_name}/")

    return new_dir_name