#!/usr/bin/env python3

import os
import sys
import argparse
import textwrap


_VERSION = 0.3

class Color:
    DEFAULT = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"
    BOLD = "\033[1m"


def parse_args():
    parser = argparse.ArgumentParser(
        prog="lsize",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent("""\
        Analyze directory disk usage.

        This tool recursively calculates directory sizes
        & file sizes and prints a readable summary.
        """),
        epilog=textwrap.dedent("""\
        Author: Pritam Behera
        GitHub: https://github.com/thelearn-tech/lsize
        License: GPL v3
        """)
    )
    parser.add_argument(
        "--version","-v",
        action="version",
        version=f"%(prog)s v{_VERSION}"
    )
    parser.add_argument(
        "path",
        help="Directory/file to analyze"
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output"
    )
    parser.add_argument(
        "-o", "--order",
        choices=["asc", "desc"],
        default="asc",
        help="Order in which the output will be displayed. default: asc."
    )
    parser.add_argument(    
        "--sort-by",   
        choices=["name", "size"],
        default="size",
        help="Based on which type the output will be displayed. default: size"
    )
    parser.add_argument(
        "--dir","-d",
        action="store_true",
        help="Only shows size of directories"
    )
    parser.add_argument(
        "--file","-f",
        action="store_true",
        help="Only shows size of files"
    )
    # parser.add_argument(
    #     "--depth",
    #     type=int,
    #     default=1,
    #     action="store_true",
    #     help="Sets the depth of the output (1[default]/2/3)"
    # )
    parser.add_argument(
        "--summarize","-s",
        action="store_true",
        help="Shows only the total directory size and counts of subdirectories and files, for quick overviews"
    
    )
    return parser.parse_args()


def get_directory_details(path): 
# Returns the total size of all files and directories in bytes, 
# along with the count of directories and files in the specified path and all subdirectories.
    total_size = 0
    dir_count = 0
    file_count = 0
    for root, dirs, files in os.walk(path):
        dir_count += 1
        for f in files:
            fp = os.path.join(root, f)
            if os.path.isfile(fp):
                file_count += 1
                total_size += os.path.getsize(fp)
    return total_size, dir_count, file_count # in bytes, int, int

def get_directory_size(path): 
    # Returns the total size of all files and directories in bytes
    total_size = 0
    for root, dirs, files in os.walk(path):
        for f in files:
            fp = os.path.join(root, f)
            if os.path.isfile(fp):
                total_size += os.path.getsize(fp)
    return total_size # in bytes


def format_size(bytes_val):
    # makes the size human readable
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes_val < 1024:
            return f"{bytes_val:.2f} {unit}"
        bytes_val /= 1024
    return f"{bytes_val:.2f} PB"


def print_sorted_output(data,path,args):
    
    
    total_dir_size = 0
    for value in data.values():
        total_dir_size += value

    if args.no_color:
        print(f'\r{path}: {format_size(total_dir_size)}              ')
    else:
        print(f'\r{Color.BLUE}{path}{Color.CYAN}: {Color.GREEN}{format_size(total_dir_size)}              ')

    sorted_list_of_tuple = "will be changed"

    if (args.order == "asc"):
        if (args.sort_by == "size"):
            sorted_list_of_tuple = sorted(data.items(), key=lambda kv: kv[1] ) # sorted dict by size asc
        else: #name
            sorted_list_of_tuple = sorted(data.items(), key=lambda kv: kv[0].lower()) #sorted dict by name asc
    else: # desc
        if (args.sort_by == "size"):
            sorted_list_of_tuple = sorted(data.items(), key=lambda kv: kv[1], reverse=True) # sorted dict by size asc
        else: #name
            sorted_list_of_tuple = sorted(data.items(), key=lambda kv: kv[0].lower(), reverse=True) #sorted dict by name asc

    lastKey = sorted_list_of_tuple[-1][0]
    symbol_format = '├──'

    if args.no_color:
        for key,value in sorted_list_of_tuple:
            if key == lastKey:
                symbol_format = '└──'
            else:
                symbol_format = '├──'

            print(f"{Color.DEFAULT}{symbol_format} {key} ({format_size(value)})")
    else: #colored
        for key,value in sorted_list_of_tuple:
            if key == lastKey:
                symbol_format = '└──'
            else:
                symbol_format = '├──'

            if key.endswith('/'):
                print(f"{Color.DEFAULT}{symbol_format} {Color.BLUE}{key} {Color.GREEN}({format_size(value)})")
            else:
                print(f"{Color.DEFAULT}{symbol_format} {key} ({Color.GREEN}{format_size(value)})")


def build_dict(path,args):
    dict_of_data = {}
    spinner = ['|', '/', '-', '\\']
    spinner_i = 0

    # Filter based on flags
    if args.dir and not args.file:  # only directories
        for entry in os.listdir(path): 
            full_path = os.path.join(path, entry)
            if os.path.isdir(full_path): #check for dir
                sub_size = get_directory_size(full_path)
                print(f'\rAnalyzing: [{spinner[spinner_i % 4]}]', end='', flush=True)
                spinner_i += 1
                dict_of_data[entry + "/"] =  sub_size

    elif args.file and not args.dir:  # only files
        for entry in os.listdir(path):
            full_path = os.path.join(path, entry)
            if os.path.isfile(full_path): # check for file
                file_size = os.path.getsize(full_path)
                print(f'\rAnalyzing: [{spinner[spinner_i % 4]}]', end='', flush=True)
                spinner_i += 1
                dict_of_data[entry] =  file_size
    
    else:  # files and directories
        for entry in os.listdir(path):
            full_path = os.path.join(path,  entry)
            if os.path.isdir(full_path):
                sub_size = get_directory_size(full_path)
                print(f'\rAnalyzing: [{spinner[spinner_i % 4]}]', end='', flush=True)
                spinner_i += 1
                dict_of_data[entry + "/"] =  sub_size
            elif os.path.isfile(full_path):
                file_size = os.path.getsize(full_path)
                print(f'\rAnalyzing: [{spinner[spinner_i % 4]}]', end='', flush=True)
                spinner_i += 1
                dict_of_data[entry] =  file_size

    return dict_of_data

def main():
    args = parse_args()
    path = args.path  # Define path from arguments

    if not os.path.exists(path): # check if path does not exist

        if args.no_color:
            print(f"Error: Path does not exist.")
        else:
            print(f"{Color.RED}Error: {Color.YELLOW}Path does not exist.")
        sys.exit(1)



    if os.path.isfile(path): # check if the path is to a file
        main_size = os.path.getsize(path)

        if args.no_color:
            print(f"Size of file '{path}': {format_size(main_size)}")
        else:
            print(f"{Color.BLUE}Size of file {Color.DEFAULT}'{path}': {Color.GREEN}{format_size(main_size)}")
        return



    if os.path.isdir(path): # dir
        if args.summarize:
            main_size,main_dir_count,main_file_count = get_directory_details(path)

            if args.no_color:
                print(f"{path}: {format_size(main_size)}")
                print(f"├─ Directory's: {main_dir_count}")
                print(f"└─ Files:     {main_file_count}\n")
            else:
                print(f"{Color.BLUE}{path}: {Color.GREEN}{format_size(main_size)}")
                print(f"{Color.DEFAULT}├─ Directory's: {Color.GREEN}{main_dir_count}")
                print(f"{Color.DEFAULT}└─ Files: {Color.GREEN}{main_file_count}\n")
            return
        else:
            data = build_dict(path,args)
            print_sorted_output(data,path,args)

    else:

        if args.no_color:
            print(f"Error: Not a valid directory.")
        else:
            print(f"{Color.RED}Error: {Color.YELLOW}Not a valid directory.")
        sys.exit(1)


if __name__ == "__main__":
    main()
