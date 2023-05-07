'''
root
├──annotations (folder)
├  ├── 1.xml
├  ├── 2.xml
├  └── n.xml
├──images (folder)
├  ├── 1.jpg
├  ├── 2.jpg
├  └── n.jpg
└──xml2yolo.py


'''
import xml.etree.ElementTree as ET
import glob
import os
import json
import argparse

#convert XML bounding box (xmin, ymin, xmax, ymax) to YOLO bounding box (x_center, y_center, width, height)
def xml_to_yolo_bbox(bbox, w, h):
    # xmin, ymin, xmax, ymax
    x_center = ((bbox[2] + bbox[0]) / 2) / w
    y_center = ((bbox[3] + bbox[1]) / 2) / h
    width = (bbox[2] - bbox[0]) / w
    height = (bbox[3] - bbox[1]) / h
    return [x_center, y_center, width, height]

#convert YOLO bounding boxes to XML bounding box
def yolo_to_xml_bbox(bbox, w, h):
    # x_center, y_center width heigth
    w_half_len = (bbox[2] * w) / 2
    h_half_len = (bbox[3] * h) / 2
    xmin = int((bbox[0] * w) - w_half_len)
    ymin = int((bbox[1] * h) - h_half_len)
    xmax = int((bbox[0] * w) + w_half_len)
    ymax = int((bbox[1] * h) + h_half_len)
    return [xmin, ymin, xmax, ymax]

def main(args):
    
    classes = []
    input_dir = args.annotations_dir
    output_dir = args.labels_dir
    image_dir = args.images_dir

    # create the labels folder (output directory)
    os.mkdir(output_dir)

    # identify all the xml files in the annotations folder (input directory)
    files = glob.glob(os.path.join(input_dir, '*.xml'))
    # loop through each 
    for fil in files:
        basename = os.path.basename(fil)
        filename = os.path.splitext(basename)[0]
        # check if the label contains the corresponding image file
        if not os.path.exists(os.path.join(image_dir, f"{filename}.jpg")):
            print(f"{filename} image does not exist!")
            continue

        result = []

        # parse the content of the xml file
        tree = ET.parse(fil)
        root = tree.getroot()
        width = int(root.find("size").find("width").text)
        height = int(root.find("size").find("height").text)

        for obj in root.findall('object'):
            label = obj.find("name").text
            # check for new classes and append to list
            if label not in classes:
                classes.append(label)
            index = classes.index(label)
            pil_bbox = [int(x.text) for x in obj.find("bndbox")]
            yolo_bbox = xml_to_yolo_bbox(pil_bbox, width, height)
            # convert data to string
            bbox_string = " ".join([str(x) for x in yolo_bbox])
            result.append(f"{index} {bbox_string}")

        if result:
            # generate a YOLO format text file for each xml file
            with open(os.path.join(output_dir, f"{filename}.txt"), "w", encoding="utf-8") as f:
                f.write("\n".join(result))

    # generate the classes file as reference
    with open('classes.txt', 'w', encoding='utf8') as f:
        f.write(json.dumps(classes))

def parse_args():
    description = \
    '''
    This script can be used to convert voc xml to YOLO format
    Usage:
    python3 xml_2_yolo.py 
        -a /fullpath/to/xml/directory -i /fullpath/to/images/directory -l /fullpath/to/textlabels/directory 
        
    '''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-a', '--annotations_dir', action='store', help='absolute path to the annotations directory ie. xmls folder', required=True)
    parser.add_argument('-i', '--images_dir', action='store', help='absolute path to images directory for corresponding xmls', required=True)
    parser.add_argument('-l', '--labels_dir', action='store', help='absolute path to directory  to save label txt files', required=True)

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    main(args)