from csv import reader
import argparse
import os
import sys
sys.path.append('../')
from utils import new_directory


def write_bbox_txt(args):
    # create a new obj folder
    obj_folder = new_directory(args.folder, os.getcwd())
    
    # load csv information
    with open(args.file) as csv_file:
        for frame in [row[0].split(' ')
                      for row in reader(csv_file, delimiter=',')][:100]:
            # corresponding image frame number
            image = frame[0].zfill(5) + '.txt'
    
            # bounding box information
            bbox = frame[2:7]
            print(' '.join(bbox))
    
            # write row data to text file
            with open(os.path.join(obj_folder, image), 'a') as f:
                f.write(' '.join(bbox))
                f.write('\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help="CSV file that contains the bbox annotations",
                        type=str)
    parser.add_argument('folder', help="Folder path to contain the outputs",
                        default='obj', type=str)
    
    args = parser.parse_args()

    write_bbox_txt(args)
    