#!/usr/bin/env python
import requests, os, sys, getopt, ast, PIL, av, numpy
from PIL import Image, ImageFont, ImageDraw
from operator import itemgetter
from datetime import datetime, timedelta

FILE_DIR = os.path.abspath(os.path.dirname(__file__))

defaut_work_dir = "../dataset_thermalRaw_no_movement"
default_thermal_mode = "4_tim"
default_file_paths = ["trained_models/thermix_28a/thermix_28a_files.txt"]
default_output_dir = "trained_models/thermix_28a/mov"
default_classes = ["1", "2"]
default_fps = 30
default_text_to_draw = None
default_add_date = False

def make_video(wd=defaut_work_dir,
               tm=default_thermal_mode,
               filepaths=default_file_paths,
               od=default_output_dir,
               classes= default_classes,
               fps=default_fps,
               text_to_draw=default_text_to_draw,
               add_date=default_add_date):

    # create the files structure
    files = {}
    for c in classes:
        files.update({c: []})

    # save frames according to class
    base_dir_path = os.path.join(FILE_DIR, wd, tm)
    for filepath in filepaths:
        print filepath
        with open(filepath, "r") as f:
            content = f.readlines()

        for l in content:
            entry = l.split()
            entry_class = entry[0]
            entry_path = os.path.join(entry[1])

            #remove last dir because entry_path include parent dir
            parent_dir_path = os.path.dirname(base_dir_path)

            entry_path = os.path.join(parent_dir_path, entry_path)

            files[entry_class].append(entry_path)

        prefix_output = os.path.basename(filepath).split('.')[0]

        output_dir = os.path.join(FILE_DIR, od)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for c in files.keys():
            print "build video for class index %s" % c
            class_paths = files[c]

            # Sort video path
            videos_path = {}
            for file in class_paths:
                if not videos_path.get(os.path.dirname(file), None):
                    videos_path[os.path.dirname(file)] = []
                name, extension = os.path.basename(file).split(".")
                videos_path[os.path.dirname(file)].append((int(name.replace("_","")), name, extension))

            class_paths = []
            for video in sorted(videos_path.keys()):
                video_frames = sorted(videos_path[video], key=itemgetter(0))
                for v in video_frames:
                    class_paths.append(os.path.join(video, "%s.%s" % v[1:]))
            # END Sort

            # make video for class
            output_path = os.path.join(output_dir, prefix_output+"_"+c+".mov")

            output = av.open(output_path, 'w')
            stream = output.add_stream("mpeg4", "%d"%fps)

            img = Image.open(class_paths[0])

            stream.height = img.size[0]
            stream.width = img.size[1]

            for path in class_paths:
                img = Image.open(path)

                if text_to_draw:
                    draw = ImageDraw.Draw(img)
                    font = ImageFont.truetype("SF-UI-Text-Medium.otf", 16)
                    draw.text((10, 75),text_to_draw,(255,255,255),font=font)

                if add_date:
                    # name_of_video = "Users_thermaldata_unkown_2016-06-20_18%3A46%3A22.000000_2"
                    name_of_video = os.path.basename(os.path.dirname(path))

                    # str_date_of_video = 2016-06-20T18%3A46%3A22
                    str_date_of_video = os.path.splitext(name_of_video).split("_")[:-2].join("T")

                    # date_of_video = datetime(2016-06-20 18:46:22)
                    date_of_video = datetime.strptime(str_date_of_video,"%Y-%m-%dT%H%%3A%M%%3A%S")

                    #convert to argentinian date
                    date_of_video -= timedelta(hours=3)


                    font = ImageFont.truetype("SF-UI-Text-Medium.otf", 14)
                    draw.text((10, 200),date_of_video.strftime("%H:%M"),(255,255,255),font=font)

                img_matrix = numpy.asarray(img)#.reshape(img.size[0], img.size[1], 3)
                frame = av.VideoFrame.from_ndarray(img_matrix)
                packet = stream.encode(frame)
                output.mux(packet)

            output.close()

def main(argv):
    new_config = {}
    try:
        opts, args = getopt.getopt(argv,"hi:o:f:t:c:",["help","input=","output=","files=",
                                                       "thermal_mode=","fps=","classes=", "text=", "add_date"])
    except getopt.GetoptError:
        print """video_from_frames.py -i <input_dir> -o <output_dir> -f '["<file_with_image_paths1>",...]' """ + \
              """--fps=<fps> -t <x_tim> -c '["class1_id", ...]' --text=<text to draw in image> --add_date"""
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print """video_from_frames.py -i <input_dir> -o <output_dir> -f '["<file_with_image_paths1>",...]' """ + \
              """--fps=<fps> -t <x_tim> -c '["class1_id", ...]' --text=<text to draw in image> --add_date"""
            sys.exit()
        elif opt in ("-i", "--input"):
            new_config["wd"] = arg
        elif opt in ("-f", "--files"):
            new_config["filepaths"] = ast.literal_eval("%s" % arg)
        elif opt in ["--fps"]:
            new_config["fps"] = int(arg)
        elif opt in ("-o", "--output"):
            new_config["od"] = arg
        elif opt in ("-c", "--classes"):
            new_config["classes"] = ast.literal_eval("%s" % arg)
        elif opt in ("-t", "--thermal_mode"):
            new_config["tm"] = arg
        elif opt in ["--text"]:
            new_config["text_to_draw"] = arg
        elif opt in ["--add_date"]:
            new_config["add_date"] = True

    make_video(**new_config)

if __name__ == "__main__":
   main(sys.argv[1:])
