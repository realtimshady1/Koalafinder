'''
Search to every .txt format file to find a specified string and
return the file location
'''
from sys import argv
from glob import glob
from tqdm import tqdm

def check_file(string, file):
    with open(file, 'r') as f:
        if string in f.read():
            print(file)

def search_labels(string, folder):
    file_list = glob(f'{folder}/*/*.txt')
    for file in tqdm(file_list):
        check_file(string, file)

    return None

if __name__=='__main__':
    if len(argv) > 2:
        string = argv[1]
        folder = argv[2]
    else:
        raise ValueError('Please enter the correct number of inputs\n1: String\n2: Frame Folder')

    search_labels(string, folder)
