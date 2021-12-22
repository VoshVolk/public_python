import sys
import os
import glob
import tempfile
import shutil
import argparse
from natsort import natsorted
import cv2

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "source",
        type=str,
        help="This is pdf source file or dir. (Specify a file or directory. Wildcards cannot be used.)"
    )
    parser.add_argument(
        "destination",
        type=str,
        nargs="?",
        default=None,
        help="This is destination file or dir."
    )
    parser.add_argument(
        "-s", "--split",
        action="store_true",
        help="Output file is a separate file."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Give more output."
    )
    return parser


def convert_pdf(f, dest_dir, split, verbose):
    if split:


        pass

    else:
        #with open()

        pass









    root, ext = os.path.splitext(f)
    name = os.path.basename(root)


def convert(source_dir, dest_dir, split, verbose):
    files = glob.glob(source_dir + "/*")
    for f in files:
        if verbose: print(f, end=" ")
        convert_pdf(f, dest_dir, split, verbose)

def alphachannel_erase(filename):
    try:
        img = cv2.imread(filename,cv2.IMREAD_UNCHANGED)
        if img.shape[2] == 4:
            img2 = cv2.imread(filename,cv2.IMREAD_COLOR)
            cv2.imwrite(filename, img2)
    except OSError as e:
        print("Error: " + filename)
        sys.exit(1)

def all_file_copy(source_dir, dest_dir):
    try:
        files = glob.glob(source_dir, "/*")
        for file in files:
            shutil.copy(file, dest_dir)
    except OSError as e:
        print("Error:" + source_dir)
        sys.exit(1)

def main():
    parser = create_parser()
    args = parser.parse_args()
    source = args.source
    split = args.split
    verbose = args.verbose

    destination = "." if args.destination is None else args.destination
    if split:
        pass
    else:
        pass
    try:
        os.makedirs(dest_dir, exist_ok=True)
    except FileExistsError as e:
        print("ERROR: Destination is " + e.filename)
        sys.exit(1)

    if os.path.isfile(source):
        root, ext = os.path.splitext(source)
        file_name = os.path.basename(root)

        if verbose: print(source, end=" > ")
        if ext == ".png":
            try:
                with tempfile.TemporaryDirectory() as dname:
                    print(dname)
                    shutil.copy(source, dname)
                    file = os.path.join(dname, file_name + ext)
                    alphachannel_erase(file)
                    convert_pdf(file, dest_dir, split, verbose)

            except OSError as e:
                print("Error: " + source)
                sys.exit(1)

        else:
            convert_pdf(source, dest_dir, split, verbose)
    
    elif os.path.isdir(source):
        png_files = glob.glob(source + "/*.png")
        if png_files == []:
            convert(source, dest_dir, split, verbose)
        else:
            with tempfile.TemporaryDirectory() as dname:
                print(dname)
                all_file_copy(source, dname)
                png_files = glob.glob(dname + "/*.png")
                for file in png_files:
                    alphachannel_erase(file)
                convert(dname, dest_dir, args.split, verbose)

    else:
        print("ERROR: Source does not exist.")
        sys.exit(1)


if __name__ == '__main__':
    main()