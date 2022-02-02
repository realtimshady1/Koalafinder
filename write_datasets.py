import os
import sys
from glob import glob

'''
Creditted to GotG@Github.com
https://github.com/GotG/yolotinyv3_medmask_demo
'''


def write_datasets(train_pct, valid_pct, source, target):
    # check extension of files in folder:
    images = glob(source + '/*/*.jpg')

    images.sort()
    number_of_images = len(images)

    index_valid = round(number_of_images * valid_pct / 100)
    index_train = round(number_of_images * train_pct / 100)
    trainfiles = images[:index_train]
    validfiles = images[index_train:(index_valid+index_train)]
    testfiles = images[(index_valid+index_train):]

    print('Number of images: ', number_of_images)

    with open(os.path.join(target,'train.txt'), mode='w') as f:
        for item in trainfiles:
            f.write(item + "\n")

    with open(os.path.join(target,'valid.txt'), mode='w') as f:
        for item in validfiles:
            f.write(item + "\n")
    with open(os.path.join(target,'test.txt'), mode='w') as f:
        for item in testfiles:
            f.write(item + "\n")
    print('Number of images for training: ', str(len(trainfiles)))
    print('Number of images for validation: ', str(len(validfiles)))
    print('Number of images for testing: ', str(len(testfiles)))


if __name__ == '__main__':
    if len(sys.argv) > 4:
        train_pct = sys.argv[1]
        valid_pct = sys.argv[2]
        source = sys.argv[3]
        target = sys.argv[4]
    else:
        raise ValueError('Please enter the correct number of inputs')

    write_datasets(train_pct, valid_pct, source, target)
