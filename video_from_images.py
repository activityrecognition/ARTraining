#!/usr/bin/env python
import requests, os, sys, getopt, ast, PIL, av, numpy
from PIL import Image

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
    od = default_output_dir

    # save frames according to class
    base_dir_path = os.path.join(FILE_DIR, wd)
    file_path = os.path.join(base_dir_path, fn)
    print file_path
    with open(file_path, "r") as f:
        content = f.readlines()

    for l in content:
        entry = l.split()
        entry_class = entry[0]
        entry_path = os.path.join(entry[1])

        #remove last dir because entry_path include parent dir
        parent_dir_path = os.path.dirname(base_dir_path)

        entry_path = os.path.join(parent_dir_path, entry_path)

        files[entry_class].append(entry_path)

    output_dir = os.path.join(FILE_DIR, od)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for c in files.keys():
        class_paths = files[c]
        class_paths = sorted(class_paths)

        output_path = os.path.join(output_dir, c+".mov")
        output = av.open(output_path, 'w')
        stream = output.add_stream("mpeg4", "10")

        img = Image.open(class_paths[0])
        stream.height = img.size[0]
        stream.width = img.size[1]

        for path in class_paths:
            img = Image.open(path)
            img_matrix = numpy.asarray(img)#.reshape(img.size[0], img.size[1], 3)
            frame = av.VideoFrame.from_ndarray(img_matrix)
            packet = stream.encode(frame)
            output.mux(packet)

        output.close()
if __name__ == "__main__":
    main()
