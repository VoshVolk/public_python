import sys
import os
import argparse
import glob
from pathlib import Path
from pdf2image import convert_from_path


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
        "-d", "--dpi",
        type=str,
        default="200",
        help="Dots per inch, can be seen as the relative resolution of the output PDF, higher is better but anything above 300 is usually not discernable to the naked eye. "
    )
    parser.add_argument(
        "-j", "--jpeg",
        action="store_true",
        help="Output format is jpeg."
    )
    parser.add_argument(
        "-p", "--png",
        action="store_true",
        help="Output format is png."
    )
    parser.add_argument(
        "-t", "--tiff",
        action="store_true",
        help="Output format is tiff."
    )
    parser.add_argument(
        "-m", "--multipage",
        action="store_true",
        help="Output format is multipage tiff."
    )
    parser.add_argument(
        "-g", "--gif",
        action="store_true",
        help="Output format is gif."
    )
    parser.add_argument(
        "-b", "--bmp",
        action="store_true",
        help="Output format is bmp."
    )
    parser.add_argument(
        "-w", "--webp",
        action="store_true",
        help="Output format is webp."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Give more output."
    )
    return parser


def convert_image(f, dest_dir, fmt, suffix, dpi, multi, verbose):
    poppler_dir = Path(__file__).parent.absolute() / "poppler/bin"
    os.environ["PATH"] += os.pathsep + str(poppler_dir)

    root, ext = os.path.splitext(f)
    name = os.path.basename(root)

    try:
        pages = convert_from_path(str(f), dpi)
        if multi:
            file_name = name + suffix
            image_path = dest_dir + "/" + file_name
            if verbose: print(end=">")
            pages[0].save(str(image_path), "TIFF", compression="tiff_deflate", save_all=True, append_images=pages[1:], dpi = (dpi, dpi))

        else:
            for i, page in enumerate(pages):
                file_name = name + "_{:03d}".format(i + 1) + suffix
                image_path = dest_dir + "/" + file_name
                if verbose: print(end=">")
                if fmt == "TIFF":
                    page.save(str(image_path), "TIFF", compression="tiff_deflate", dpi = (dpi, dpi))

                else:
                    page.save(str(image_path), fmt, dpi = (dpi, dpi))
        
        if verbose: print(" <Success>", dest_dir)

    except OSError as e:
        print("Error: " + f.title)
        pass


def main():
    parser = create_parser()
    args = parser.parse_args()
    dpi = int(args.dpi)
    verbose = args.verbose
    j = args.jpeg
    p = args.png
    t = args.tiff
    m = args.multipage
    g = args.gif
    b = args.bmp
    w = args.webp
    opt = [j, p, t, m, g, b, w]

    if opt.count(True) == 1:
        fmt , suffix = ("JPEG", ".jpg") if j else ("PNG", ".png") if p else ("TIFF", ".tif") if t or m else ("GIF", ".gif") if g else ("BMP", ".bmp") if b else ("WEBP", ".webp")
        if verbose: print("Image format:", fmt)

    else:
        print("Error: Any one of jpeg, png, tiff, multipage tiff, gif, bmp, webp.")
        sys.exit(1)

    dest_dir = "." if args.destination is None else args.destination
    try:
        os.makedirs(dest_dir, exist_ok=True)
    except FileExistsError as e:
        print("ERROR: Destination is " + e.filename)
        sys.exit(1)

    if os.path.isfile(args.source):
        root, ext = os.path.splitext(args.source)
        if ext != ".pdf":
            print("Error: PDF file does not exist.")
            sys.exit(1)
        if verbose: print(args.source, end=" > ")
        convert_image(args.source, dest_dir, fmt, suffix, dpi, m, verbose)
    
    elif os.path.isdir(args.source):
        files = glob.glob(args.source + "/*.pdf")
        for f in files:
            if verbose: print(f, end=" ")
            convert_image(f, dest_dir, fmt, suffix, dpi, m, verbose)

    else:
        print("ERROR: Source file or dir does not exist.")
        sys.exit(1)


if __name__ == '__main__':
    main()