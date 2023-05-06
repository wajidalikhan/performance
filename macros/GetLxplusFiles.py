#!/usr/bin/env python
"""
python GetLxplusFiles.py /path/to/files /path/to/output.txt

"""
import os, argparse

def find_files_by_extension(paths, extension):
    """
    Returns a list of all files with a given extension
    in a list of directories and their subdirectories.
    """
    file_list = []
    for path in paths:
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith(extension):
                    file_list.append(os.path.join(root, file))
    return file_list

def save_file_list(file_list, output_file):
    """
    Saves a list of file paths to a text file.
    """
    with open(output_file, "w") as f:
        for file_path in file_list:
            f.write(file_path + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Collects all files of a given type in all subfolders in a given path into a text file.")
    parser.add_argument("input_paths", nargs="+", help="the directory path(s) to search")
    parser.add_argument("output_file", help="the output file name")
    parser.add_argument("-e", "--extension", default=".root", help="the file extension to search for (default: .root)")
    args = parser.parse_args()
    
    file_list = find_files_by_extension(args.input_paths, args.extension)
    save_file_list(file_list, args.output_file)
    print(f"Found {len(file_list)} files with extension {args.extension}.")
