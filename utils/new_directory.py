import os

def new_directory(dir_name, dir_location):
    """
    Create a directory if it does not exist

    dir_name: name of the target directory
    dir_location: location of the target directory

    new_dir_name: location inside the new target directory
    """
    # check if folder exists
    if os.path.exists(os.path.join(dir_location, dir_name)):
        print(f"Using existing folder {dir_name}/")
        return os.path.join(dir_location, dir_name)
    else:
        new_dir_name = os.path.join(dir_location, dir_name)
        os.mkdir(new_dir_name)
        print(f"Created new folder {dir_name}/")

    return new_dir_name