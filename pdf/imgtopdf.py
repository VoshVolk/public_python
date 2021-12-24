import sys
import os
import glob
import tempfile
import shutil
import argparse
import img2pdf
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
        help="Output file is a separate file. Pdf filename follows image file."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Give more output."
    )
    return parser

def convert_pdf(input, output, source, destination, split, verbose):
    input_list = glob.glob(input + "/*")

    if split:
        for file in natsorted(input_list):
            origin_source = os.path.join(source, os.path.basename(file))
            single_convert_pdf(file, output, origin_source, destination, verbose)

    else:
        if verbose: print(source + "*", end=" > ")
        if output == "":
            output = os.path.join(destination, "new.pdf")

        try:
            with open(output, "wb") as f:
                f.write(img2pdf.convert([str(i) for i in natsorted(input_list)]))
        except Exception as e:
            print(e)
            sys.exit(1)
        
        if verbose: print(output)

def single_convert_pdf(input, output, source, destination, verbose):
    if verbose: print(source, end=" > ")
    if output == "":
        root, ext = os.path.splitext(input)
        file_name = os.path.basename(root)
        output = os.path.join(destination, file_name + ".pdf")
    
    try:
        with open(output, "wb") as f:
            f.write(img2pdf.convert([input]))
    except Exception as e:
        print(e)
        sys.exit(1)

    if verbose: print(output)

def alphachannel_erase(filename):
    try:
        img = cv2.imread(filename,cv2.IMREAD_UNCHANGED)
        if img.shape[2] == 4:
            img2 = cv2.imread(filename,cv2.IMREAD_COLOR)
            cv2.imwrite(filename, img2)
    except Exception as e:
        print(e)
        sys.exit(1)

def makedir(path):
    try:
        os.makedirs(path, exist_ok=True)
    except FileExistsError as e:
        print("ERROR: Destination is " + e.filename)
        sys.exit(1)


def main():
    parser = create_parser()
    args = parser.parse_args()
    source = args.source
    split = args.split
    verbose = args.verbose

    output = ""
    destination = "." if args.destination is None else args.destination
    if split:
        if destination.endswith(".pdf"):
            makedir(os.path.dirname(destination))
            destination = os.path.dirname(destination)
        else:
            makedir(destination)

    else:
        if destination.endswith(".pdf"):
            makedir(os.path.dirname(destination))
            output = destination
            destination = os.path.dirname(destination)
        else:
            makedir(destination)

    if verbose: print("**** Start ****")
    if os.path.isfile(source):
        root, ext = os.path.splitext(source)
        file_name = os.path.basename(root)

        if ext == ".png":
            try:
                with tempfile.TemporaryDirectory() as dname:
                    shutil.copy(source, dname)
                    input = os.path.join(dname, file_name + ext)
                    alphachannel_erase(input)
                    single_convert_pdf(input, output, source, destination, verbose)
            except Exception as e:
                print(e)
                sys.exit(1)

        else:
            single_convert_pdf(source, output, source, destination, verbose)
    
    elif os.path.isdir(source):
        png_files = glob.glob(source + "/*.png")

        if png_files == []:
            convert_pdf(source, output, source, destination, split, verbose)

        else:
            try:
                with tempfile.TemporaryDirectory() as dname:
                    shutil.copytree(source, dname, dirs_exist_ok=True)
                    png_files = glob.glob(dname + "/*.png")
                    for file in png_files:
                        alphachannel_erase(file)
                    convert_pdf(dname, output, source, destination, split, verbose)
            except Exception as e:
                print(e)
                sys.exit(1)

    else:
        print("ERROR: Source does not exist.")
        sys.exit(1)

    if verbose: print("**** Complete! ****")


if __name__ == '__main__':
    main()