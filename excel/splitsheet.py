import os
import sys
import argparse
import openpyxl
import copy

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "excel_file",
        type=str,
        help="This is a Excel file. (Supported formats are: .xlsx,.xlsm,.xltx,.xltm. And wildcards cannot be used. )"
    )
    parser.add_argument(
        "dest_dir",
        type=str,
        nargs="?",
        default=None,
        help="This is a destination dir."
    )
    return parser

def split(excel_file, dest_dir):
    try:
        book = openpyxl.load_workbook(excel_file)
        print("EXCEL FILE: " + excel_file)
        for sheet in book:
            file_name = dest_dir + "/" + sheet.title + ".xlsx"
            print(file_name)
            new_book = copy.deepcopy(book)
            for new_sheet in new_book:
                if new_sheet.title == sheet.title:
                    continue
                else:
                    new_book.remove(new_sheet)
            new_book.save(file_name)
        book.close()
        print("COMPLETE!")
    except:
        print("ERROR:")
        print(sys.exc_info()[1])
        sys.exit(1)


def main():
    parser = create_parser()
    args = parser.parse_args()

    if not os.path.isfile(args.excel_file):
        print("ERROR: Excel file does not exist.")
        sys.exit(1)
    
    if args.dest_dir is None:
        dest_dir = "."
    else:
        dest_dir = args.dest_dir
    
    try:
        os.makedirs(dest_dir, exist_ok=True)
    except FileExistsError as e:
        print("ERROR: dest_dir is " + e.filename)
        sys.exit(1)
    
    split(args.excel_file, dest_dir)


if __name__ == '__main__':
    main()