from csv import reader
import argparse
import os
import sys
sys.path.append('../')
from utils import new_directory


def write_bbox_txt(args):
    # create a new obj folder
    obj_folder = new_directory(args.folder, './')
    
    # load csv information
    with open(args.file) as csv_file:
        for frame in [row[0].split(' ')
                      for row in reader(csv_file, delimiter=',')][:100]:
            # corresponding image frame number
            image = frame[0].zfill(5) + '.txt'
    
            # bounding box information
            bbox = []
            bbox.append(frame[2])
            bbox.append(int(frame[3])/args.width)
            bbox.append(int(frame[4])/args.width)
            bbox.append(int(frame[5])/args.height)
            bbox.append(int(frame[6])/args.height)
            
            # write row data to text file
            with open(os.path.join(obj_folder, image), 'w') as f:
                f.write(' '.join(map(str,bbox)))
                f.write('\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help="CSV file that contains the bbox annotations",
                        type=str)
    parser.add_argument('folder', help="Folder path to contain the outputs",
                        default='obj', type=str)
    parser.add_argument('-width', help="width of the image",
                        default=640, type=int)
    parser.add_argument('-height', help="height of the image",
                        default=512, type=int)
    
    args = parser.parse_args()

    write_bbox_txt(args)
    