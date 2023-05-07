import os
import argparse
from PIL import Image, ImageDraw


def yolo_to_xml_bbox(bbox, w, h):
    w_half_len = (bbox[2] * w) / 2
    h_half_len = (bbox[3] * h) / 2
    xmin = int((bbox[0] * w) - w_half_len)
    ymin = int((bbox[1] * h) - h_half_len)
    xmax = int((bbox[0] * w) + w_half_len)
    ymax = int((bbox[1] * h) + h_half_len)
    return [xmin, ymin, xmax, ymax]


def draw_image(img, bboxes):
    draw = ImageDraw.Draw(img)
    for bbox in bboxes:
        draw.rectangle(bbox, outline="red", width=2)
    img.save("example.jpg")
    img.show()

def main(args):
    
    image_filename = args.image_path
    label_filename = args.labeltext_path
    bboxes = []

    img = Image.open(image_filename)

    with open(label_filename, 'r', encoding='utf8') as f:
        for line in f:
            data = line.strip().split(' ')
            bbox = [float(x) for x in data[1:]]
            bboxes.append(yolo_to_xml_bbox(bbox, img.width, img.height))

    draw_image(img, bboxes)

def parse_args():
    description = \
    '''
    This script can be used to visualise yolo annotations
    Usage:
    python3 visualise_yolo_annotations.py 
        -i /fullpath/to/image -l /fullpath/to/textlabel
    
    '''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-i', '--image_path', action='store', help='absolute path to the image file', required=True)
    parser.add_argument('-l', '--labeltext_path', action='store', help='absolute path to image label text file', required=True)
           
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    main(args)

