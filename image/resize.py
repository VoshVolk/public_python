import os
import sys
import argparse
import glob
import re
from PIL import Image
from decimal import Decimal, getcontext, FloatOperation, ROUND_HALF_UP

getcontext().traps[FloatOperation] = True


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "source",
        type=str,
        help="This is source. (Specify a file or directory. Wildcards cannot be used.)"
    )
    parser.add_argument(
        "dest_dir",
        type=str,
        nargs="?",
        default=None,
        help="This is destination dir."
    )
    parser.add_argument(
        "-s", "--size",
        type=str,
        required=True,
        help="This is size parameter. ex.) 800, 600x400, 350x240!, 450x, x400 etc."
    )
    parser.add_argument(
        "-f", "--filter",
        type=str,
        choices=["NEAREST", "BOX", "BILINEAR", "HAMMING", "BICUBIC", "LANCZOS"],
        help="This is filter parameter."
    )
    parser.add_argument(
        "-t", "--thumbnail",
        action="store_true",
        help="This is thumbnail option. Fixed aspect ratio."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Give more output."
    )
    return parser


def resize(f, arg_size, dest_dir, resample, thumbnail, verbose):
    size_opt = arg_size.lower()
    x_pos = size_opt.find("x")
    width_str = size_opt[:x_pos]
    height_str= size_opt[x_pos + 1:]
    non_ope = False

    try: ######### File open
        img = Image.open(f)
        
        try: ######### Size option check
            w_spec = get_size(width_str, img.width)
            h_spec = get_size(height_str, img.height)

            if not thumbnail:
                if x_pos == -1: ######### Width only
                    w = get_size(size_opt, img.width)
                    width, height = ref_width(w, img)

                else: ############ Width & height

                    if height_str == "": # Fixed aspect ratio
                        width, height = ref_width(w_spec, img)
                    
                    elif width_str == "": # Fixed aspect ratio
                        width, height = ref_height(h_spec, img)

                    elif size_opt[-1] == "!": # Ignore aspect ratio
                        width ,height = w_spec, h_spec

                    elif size_opt[-1] == ">": # Fixed aspect ratio
                        if img.width > w_spec and img.height > h_spec:
                            width, height = adapt_size(size_opt, img)
                        else:
                            non_ope = True

                    elif size_opt[-1] == "<": # Fixed aspect ratio
                        if img.width < w_spec and img.height < h_spec:
                            width, height = adapt_size(size_opt, img)
                        else:
                            non_ope = True

                    elif size_opt[-1] == "^": # Fixed aspect ratio
                        if img.width < img.height:
                            width, height = ref_width(w_spec, img)
                        else:
                            width, height = ref_height(h_spec, img)

                    else: # Fixed aspect ratio
                        width, height = adapt_size(size_opt, img)

        except:
            print("ERROR: Invalid size option.")
            sys.exit(1)

        if non_ope and verbose:
            print("Non operation: ", f)
        
        else:
            root, ext = os.path.splitext(f)
            file_name = os.path.basename(root)

            if thumbnail:
                img.thumbnail((w_spec, h_spec), resample)
                img.save(os.path.join(dest_dir, file_name + ext))
                if verbose:
                    print("Success <Thumbnail> <%sx%s>: " % (w_spec, h_spec) + dest_dir + "/" + file_name + ext)
            else:
                img_resize = img.resize((int(width), int(height)), resample)
                img_resize.save(os.path.join(dest_dir, file_name + ext))
                if verbose:
                    print("Success <Resize> <%sx%s>: " % (width, height) + dest_dir + "/" + file_name + ext)

    except OSError as e:
        print("Error: ", f)
        pass

def adapt_size(size_opt, img) -> tuple[Decimal, Decimal]:
    x_pos = size_opt.find("x")
    width_str = size_opt[:x_pos]
    height_str= size_opt[x_pos + 1:]
    w_spec = get_size(width_str, img.width)
    h_spec = get_size(height_str, img.height)

    if img.width >= img.height:
        w_temp, h_temp = ref_width(w_spec, img)
        if h_temp > h_spec:
            return ref_height(h_spec, img)

    else:
        w_temp, h_temp = ref_height(h_spec, img)
        if w_temp > w_spec:
            return ref_width(w_spec, img)

    return w_temp, h_temp

def ref_width(w_spec, img) -> tuple[Decimal, Decimal]:
    try:
        height = round_halfup(img.height * w_spec / img.width)
        return w_spec, height
    except:
        sys.exit(1)

def ref_height(h_spec, img) -> tuple[Decimal, Decimal]:
    try:
        width = round_halfup(img.width * h_spec / img.height)
        return width, h_spec
    except:
        sys.exit(1)

def get_size(size_str, source_size) -> Decimal:
    if size_str == "": return
    scale = percent(size_str)
    try:
        if scale is None:
            return Decimal("".join(filter(str.isdigit, size_str)))
        else:
            ratio = Decimal("".join(filter(lambda s:re.sub(r"[^\d.]", "", s), scale)))
            return round_halfup(source_size * ratio / 100)
    except:
        sys.exit(1)

def percent(s) -> str:
    unit_pos = s.find("%")
    if unit_pos == -1:
        return None
    else:
        return s[:unit_pos]

def round_halfup(decimal_value) -> Decimal:
    return decimal_value.quantize(Decimal('0'), rounding=ROUND_HALF_UP)


def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.filter is None:
        resample = Image.NEAREST
    else:
        filter_arg = args.filter.upper()
        if filter_arg == "NEAREST":
            resample = Image.NEAREST
        elif filter_arg == "BOX":
            resample = Image.BOX
        elif filter_arg == "BILINEAR":
            resample = Image.BILINEAR
        elif filter_arg == "HAMMING":
            resample = Image.HAMMING
        elif filter_arg == "BICUBIC":
            resample = Image.BICUBIC
        elif filter_arg == "LANCZOS":
            resample = Image.LANCZOS
        else:
            resample = Image.NEAREST
    
    dest_dir = "." if args.dest_dir is None else args.dest_dir
    try:
        os.makedirs(dest_dir, exist_ok=True)
    except FileExistsError as e:
        print("ERROR: dest_dir is " + e.filename)
        sys.exit(1)

    if os.path.isfile(args.source):
        resize(args.source, args.size, dest_dir, resample, args.thumbnail, args.verbose)
    
    elif os.path.isdir(args.source):
        files = glob.glob(args.source + "/*")
        for f in files:
            resize(f, args.size, dest_dir, resample, args.thumbnail, args.verbose)

    else:
        print("ERROR: Source file or dir does not exist.")
        sys.exit(1)


if __name__ == '__main__':
    main()