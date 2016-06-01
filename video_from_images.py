#!/usr/bin/env python
import requests, os, sys, getopt, ast

# FILE_DIR = os.path.abspath(os.path.dirname(__file__))
FILE_DIR = os.path.abspath(os.path.dirname("."))
defaut_work_dir = "dataset/4_tim"
default_file_name = "thermix_1_training.txt"
default_output_dir = "mov"

classes = ["1", "3", "4"]
files = {}


def main():
    # create the files structure
    for c in classes:
        files.update({c: []})

    wd = defaut_work_dir
    fn = default_file_name

    # save frames according to class
    file_url = os.path.join(FILE_DIR, wd, fn)
    with open(file_url, "r") as f:
        content = f.readlines()
        for l in content:
            entry = l.split()
            file_class = entry[0]
            file_url = entry[1]

            files[file_class].append(file_url)


if __name__ == "__main__":
    main()
