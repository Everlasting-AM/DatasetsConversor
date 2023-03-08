import argparse
from decimal import Decimal
import os
import shutil

def add_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--images_input", type=str, required=True)
    parser.add_argument("--labels_input", type=str, required=True)
    parser.add_argument("--output_images", type=str, required=True)
    parser.add_argument("--output_labels", type=str, required=True)
    parser.add_argument("--selected_part", type=Decimal, required=True)
    return parser

def extract_elemens(part: Decimal, images_dir: str):
    print
    num_elems = len(os.listdir(images_dir))
    return os.listdir(images_dir)[:int(num_elems * part)]

def copy_elemens(selected: list[str], dir: str):
    if not os.path.isdir(dir):
        os.makedirs(dir)
    for elem in selected:
        filename_base = os.path.basename(elem)
        print("Copiado:", shutil.copy(elem, os.path.join(dir, filename_base)))

def copy_labels(fileimages: list[str], dir_labels: str, dir_dest: str):
    if not os.path.isdir(dir_dest):
        os.makedirs(dir_dest)
    for fname in fileimages:
        name, ext = os.path.splitext(fname)
        label_name = name + ".txt"
        shutil.copy(os.path.join(dir_labels, label_name), os.path.join(dir_dest))


def main():
    parser = add_arguments()
    args = parser.parse_args()
    selected = extract_elemens(args.selected_part, args.images_input)
    copy_elemens([os.path.join(args.images_input, file) for file in selected], args.output_images)
    copy_labels(selected, args.labels_input, args.output_labels)
    
if __name__ == '__main__':
    main()