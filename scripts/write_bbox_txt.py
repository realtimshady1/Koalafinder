from csv import reader
import sys
import os

sys.path.append('../src')
from utils import new_directory

file = 'koala_tracked_all.csv'
folder = 'obj'

# create a new obj folder
# obj_folder = new_directory(folder, os.getcwd())

# load csv information
with open(file) as csv_file:
    for frame in [row[0].split(' ') for row in reader(csv_file, delimiter=',')][:100]:
        # corresponding image frame number
        image = frame[0].zfill(5) + '.txt'
        
        # bounding box information
        bbox = frame[2:7]
        print(' '.join(bbox))
        
        # write row data to text file
        with open(os.path.join(folder, image), 'a') as f:
            f.write(' '.join(bbox))
            f.write('\n')
            
    



# if __name__ == '__main__':
#     if len(sys.argv) < 2:
#         raise Exception('Please specify a file path.')
#     file = sys.argv[1]
    