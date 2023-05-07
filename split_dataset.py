import random
import glob
import os
import shutil
import argparse


def copyfiles(fil, root_dir, image_dir, label_dir):
    basename = os.path.basename(fil)
    filename = os.path.splitext(basename)[0]

    # copy image
    src = fil
    dest = os.path.join(root_dir, image_dir, f"{filename}.jpg")
    shutil.copyfile(src, dest)

    # copy annotations
    src = os.path.join(label_dir, f"{filename}.txt")
    dest = os.path.join(root_dir, label_dir, f"{filename}.txt")
    if os.path.exists(src):
        shutil.copyfile(src, dest)

def main(args):
    
    image_dir = args.image_dir
    label_dir = args.label_dir
    train_part = args.train_ratio

    valid_part = args.valid_ratio
    test_part = args.test_ratio

    lower_limit = 0
    files = glob.glob(os.path.join(image_dir, '*.jpg'))

    random.shuffle(files)

    folders = {"train": train_part, "val": valid_part, "test": test_part}
    check_sum = sum([folders[x] for x in folders])

    assert check_sum == 1.0, "Split proportion is not equal to 1.0"

    for folder in folders:
        os.mkdir(folder)
        temp_label_dir = os.path.join(folder, label_dir)
        os.mkdir(temp_label_dir)
        temp_image_dir = os.path.join(folder, image_dir)
        os.mkdir(temp_image_dir)

        limit = round(len(files) * folders[folder])
        for fil in files[lower_limit:lower_limit + limit]:
            copyfiles(fil, folder, image_dir, label_dir)
        lower_limit = lower_limit + limit

def parse_args():
    description = \
    '''
    This script can be used to split yolo type dataset
    Usage:
    python3 vsplit_dataset.py 
        -i /fullpath/to/images/dir -l /fullpath/to/textlabels/dir
    
    '''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-i', '--image_dir', action='store', help='absolute path to the image directory', required=True)
    parser.add_argument('-l', '--label_dir', action='store', help='absolute path to label directory', required=True)
    parser.add_argument('-t', '--train_ratio', action='store', help='training dataset ratio', type=float, default=0.85, required=False)
    parser.add_argument('-v', '--valid_ratio', action='store', help='training dataset ratio', type=float, default=0.1, required=False)
    parser.add_argument('-x', '--test_ratio', action='store', help='training dataset ratio', type=float, default=0.05, required=False)
           
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    main(args)