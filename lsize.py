#!/usr/bin/env python3

import os
import sys
import argparse
import textwrap


_VERSION = 0.2

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
    return total_size # in bytes, int, int


def format_size(bytes_val):
    # makes the size human readable
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes_val < 1024:
            return f"{bytes_val:.2f} {unit}"
        bytes_val /= 1024
    return f"{bytes_val:.2f} PB"


def print_size_colored(path,args):

    print(f"\n{Color.GREEN}Analyzing: {Color.DEFAULT}{path.rstrip('/')}/ ")
    main_size = get_directory_size(path)
    print(f"{Color.BLUE}{path.rstrip('/')}/{Color.DEFAULT}: ", end='')
    print(f"{Color.GREEN}{format_size(main_size)}{Color.DEFAULT} ", end='')

    # Filter based on flags
    if args.dir and not args.file:  # only directories
        print("(Subdirectory only)")
        for entry in os.listdir(path):
            full_path = os.path.join(path, entry)
            if os.path.isdir(full_path):
                sub_size = get_directory_size(full_path)
                print(f"{Color.DEFAULT}├── {Color.BLUE}{entry}/ {Color.GREEN}({format_size(sub_size)})")
    
    elif args.file and not args.dir:  # only files
        print("(File only)")
        for entry in os.listdir(path):
            full_path = os.path.join(path, entry)
            if os.path.isfile(full_path):
                file_size = os.path.getsize(full_path)
                print(f"{Color.DEFAULT}├── {entry} ({Color.GREEN}{format_size(file_size)})")
    
    else:  # show files and directories
        print('')
        for entry in os.listdir(path):
            full_path = os.path.join(path,  entry)
            if os.path.isdir(full_path):
                sub_size = get_directory_size(full_path)
                print(f"{Color.DEFAULT}├── {Color.BLUE}{entry}/ {Color.GREEN}({format_size(sub_size)})")
            elif os.path.isfile(full_path):
                file_size = os.path.getsize(full_path)
                print(f"{Color.DEFAULT}├── {entry} ({Color.GREEN}{format_size(file_size)})")

def print_size_no_color(path,args):

    print(f"\nAnalyzing: {path.rstrip('/')}/ ")
    
    main_size = get_directory_size(path)
    
    print(f"{path.rstrip('/')}/: ", end='')
    print(f"{format_size(main_size)} ", end='')

    # Filter based on flags
    if args.dir and not args.file:  # only directories
        print("(Subdirectory only)")
        for entry in os.listdir(path):
            full_path = os.path.join(path, entry)
            if os.path.isdir(full_path):
                sub_size = get_directory_size(full_path)
                print(f"{Color.DEFAULT}├── {entry}/ ({format_size(sub_size)})")
    
    elif args.file and not args.dir:  # only files
        print("(File only)")
        for entry in os.listdir(path):
            full_path = os.path.join(path, entry)
            if os.path.isfile(full_path):
                file_size = os.path.getsize(full_path)
                print(f"{Color.DEFAULT}├── {entry} ({format_size(file_size)})")
    
    else:  # show files and directories
        print('')
        for entry in os.listdir(path):
            full_path = os.path.join(path,  entry)
            if os.path.isdir(full_path):
                sub_size = get_directory_size(full_path)
                print(f"{Color.DEFAULT}├── {entry}/ ({format_size(sub_size)})")
            elif os.path.isfile(full_path):
                file_size = os.path.getsize(full_path)
                print(f"{Color.DEFAULT}├── {entry} ({format_size(file_size)})")


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
                print(f"{path}/: {format_size(main_size)}")
                print(f"├──── Directory's: {main_dir_count}")
                print(f"├──── Files:     {main_file_count}\n")
            else:
                print(f"{Color.BLUE}{path}/: {Color.GREEN}{format_size(main_size)}")
                print(f"{Color.DEFAULT}├──── Directory's: {Color.GREEN}{main_dir_count}")
                print(f"{Color.DEFAULT}├──── Files:     {Color.GREEN}{main_file_count}\n")
            return
        else:
            if args.no_color:
                print_size_no_color(path,args)
            else:
                print_size_colored(path,args)
    else:

        if args.no_color:
            print(f"Error: Not a valid directory.")
        else:
            print(f"{Color.RED}Error: {Color.YELLOW}Not a valid directory.")
        sys.exit(1)


if __name__ == "__main__":
    main()
