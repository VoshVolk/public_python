import os
import sys
import argparse
import glob
from PIL import Image, ImageDraw
import numpy as np


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "source",
        type=str,
        help="This is source file or dir. (Specify a file or directory. Wildcards cannot be used.)"
    )
    parser.add_argument(
        "destination",
        type=str,
        nargs="?",
        default=None,
        help="This is destination file or dir."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Give more output."
    )
    return parser

def select_color(color):
    mean = np.array(color).mean(axis=0)
    return (255,255,255,0) if mean >= 250 else color

def transparent(img):
    w, h = img.size
    transparent_img = Image.new('RGBA', (w, h))
    np.array([[transparent_img.putpixel((x, y), select_color(img.getpixel((x,y)))) for x in range(w)] for y in range(h)])
    return transparent_img

def trans(f, dst_dir, verbose):
    try:
        original_img = Image.open(f).convert("RGB")
        root, ext = os.path.splitext(f)
        file_name = os.path.basename(root)
        transparent(original_img).save(os.path.join(dst_dir, file_name + ".png"))
        if verbose:
            print("Success Transparent: " + dst_dir + file_name + ".png")
    except OSError as e:
        print("Error: " + f.title)
        pass


def main():
    parser = create_parser()
    args = parser.parse_args()

    dest_dir = "." if args.destination is None else args.destination
    try:
        os.makedirs(dest_dir, exist_ok=True)
    except FileExistsError as e:
        print("ERROR: Destination is " + e.filename)
        sys.exit(1)

    if os.path.isfile(args.source):
        trans(args.source, dest_dir, args.verbose)
    
    elif os.path.isdir(args.source):
        files = glob.glob(args.source + "/*")
        for f in files:
            trans(f, dest_dir, args.verbose)

    else:
        print("ERROR: Source file or dir does not exist.")
        sys.exit(1)


if __name__ == '__main__':
    main()