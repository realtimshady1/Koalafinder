import os
import argparse
from collections import Counter

'''
Creditted to GotG@Github.com
https://github.com/GotG/yolotinyv3_medmask_demo
'''


def write_datasets(args):
    extensions = []
    images = []
    # check extension of files in folder:
    for filename in os.scandir(args.source):
        title, ext = os.path.splitext(filename.name)
        if ext != ".txt":
            extensions.append(ext)

    ext_dict = Counter(extensions)
    extension = max(ext_dict, key=ext_dict.get)
    print("Your image file extension is: " + extension)

    for filename in os.listdir(args.source):
        _, ext = os.path.splitext(os.path.basename(filename))
        if ext == extension:
            images.append(os.path.join(args.source, filename))

    images.sort()
    number_of_images = len(images)

    index_valid = round(number_of_images * args.valid_pct / 100)
    index_train = round(number_of_images * args.train_pct / 100)
    trainfiles = images[:index_train]
    validfiles = images[index_train:(index_valid+index_train)]
    testfiles = images[(index_valid+index_train):]

    print('Number of images:', number_of_images)

    with open(os.path.join(args.target,'train.txt'), mode='w') as f:
        for item in trainfiles:
            f.write(item + "\n")

    with open(os.path.join(args.target,'valid.txt'), mode='w') as f:
        for item in validfiles:
            f.write(item + "\n")
    with open(os.path.join(args.target,'test.txt'), mode='w') as f:
        for item in testfiles:
            f.write(item + "\n")
    print('Number of images used for training', str(len(trainfiles)))
    print('Number of images used for validation', str(len(validfiles)))
    print('Number of images used for testing', str(len(testfiles)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('train_pct', help="percentage of images to be used for training, the rest are used for validation and testing",
                        type=int)
    parser.add_argument('valid_pct', help="percentage of images to be used for validation, the rest are used for training and testing",
                        type=int)
    parser.add_argument('source', help="path to directory with images and yolo annotations",
                        type=str)
    parser.add_argument('-target', help="path to directory to save the generated outputs",
                        type=str, default='./')
    args = parser.parse_args()

    write_datasets(args)
