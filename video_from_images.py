#!/usr/bin/env python
import requests, os, sys, getopt, ast, PIL, av, numpy as np
from PIL import Image, ImageFont, ImageDraw
from operator import itemgetter
from datetime import datetime, timedelta

import shutil

FILE_DIR = os.path.abspath(os.path.dirname(__file__))

defaut_work_dir = "./trained_models/thermix_28b/classification_output"
default_thermal_mode = "14_tim"
default_file_paths = ["trained_models/thermix_28b/classification_output/4_tim/thermix_1_files.txt"]
default_output_dir = "../mov_suenos_dorados"
default_classes = ["3"]
default_fps = 60
default_text_to_draw = None
default_add_date = False
default_add_frame_id = False
default_stretch_frames = False

def imhist(im):
    m, n = im.shape
    h = [0.0] * 256
    for i in range(m):
        for j in range(n):
            h[im[i, j]]+=1
    return np.array(h)/(m*n)

def cumsum(h):
    # finds cumulative sum of a numpy array, list
    return [sum(h[:i+1]) for i in range(len(h))]

def histeq(im):
    #calculate Histogram
    h = imhist(im)
    cdf = np.array(cumsum(h)) #cumulative distribution function
    sk = np.uint8(255 * cdf) #finding transfer function values
    s1, s2 = im.shape
    Y = np.zeros_like(im)
    # applying transfered values for each pixels
    for i in range(0, s1):
        for j in range(0, s2):
            Y[i, j] = sk[im[i, j]]
    H = imhist(Y)
    #return transformed image, original and new istogram, 
    # and transform function
    return Y , h, H, sk

def hist_stretching(im_asarray):
    mi = im_asarray.min()
    ma = im_asarray.max()
    gap = 255 / (ma - mi)
    
    Y = np.zeros_like(im_asarray)
    s1, s2 = im_asarray.shape

    for i in range(0, s1):
        for j in range(0, s2):
            Y[i, j] = (im_asarray[i, j] - mi) * gap
    
    return Y

def make_video(wd=defaut_work_dir,
               tm=default_thermal_mode,
               filepaths=default_file_paths,
               od=default_output_dir,
               classes= default_classes,
               fps=default_fps,
               text_to_draw=default_text_to_draw,
               add_date=default_add_date,
               add_frame_id=default_add_frame_id,
               stretch_frames=default_stretch_frames):

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
            if not entry_class in classes:
                continue
            
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
            stream = output.add_stream("mpeg4", "%d" % fps)

            img = Image.open(class_paths[0])
            
            stream.height = img.size[0]
            stream.width = img.size[1]
            
            for frame_id,path in enumerate(class_paths):
                print "%d %s" %(frame_id,path)
                if not path.endswith('.png'):
                    continue

                img = Image.open(path)

                if img.mode != "RGB":
                    img=img.convert("RGB")

                if stretch_frames:
                    img = np.asarray(img) 

                    r = img[:,:,0]
                    eq_1 = hist_stretching(r)
                    img = Image.fromarray(eq_1, 'L')

                    if img.mode != "RGB":
                        img=img.convert("RGB")
                        
                if text_to_draw:
                    draw = ImageDraw.Draw(img)
                    font = ImageFont.truetype("SF-UI-Text-Medium.otf", 16)
                    draw.text((10, 75),text_to_draw,(255,255,255),font=font)

                if add_date:
                    # name_of_video = "Users_thermaldata_unkown_2016-06-20_18%3A46%3A22.000000_2"
                    name_of_video = os.path.basename(os.path.dirname(path))

                    # str_date_of_video = 2016-06-20T18%3A46%3A22
                    str_date_of_video = "T".join(os.path.splitext(name_of_video)[0].split("_")[-2:])

                    # date_of_video = datetime(2016-06-20 18:46:22)
                    date_of_video = datetime.strptime(str_date_of_video,"%Y-%m-%dT%H%%3A%M%%3A%S")

                    #convert to argentinian date
                    date_of_video -= timedelta(hours=3)
                    
                    font = ImageFont.truetype("SF-UI-Text-Medium.otf", 12)
                    draw = ImageDraw.Draw(img)
                    draw.text((10, 200),date_of_video.strftime("%Y-%m-%d %H:%M"),(255,255,255),font=font)

                if add_frame_id:
                    font = ImageFont.truetype("SF-UI-Text-Medium.otf", 18)
                    draw = ImageDraw.Draw(img)
                    draw.text((180, 210),str("%6d"%frame_id),(255,255,255),font=font)
                    
                img_matrix = np.asarray(img)
                frame = av.VideoFrame.from_ndarray(img_matrix)
                packet = stream.encode(frame)
                output.mux(packet)

            output.close()
            print "finished composing images for ffmpeg"
    
def main(argv):
    new_config = {}
    try:
        opts, args = getopt.getopt(argv,"hi:o:f:t:c:",["help","input=","output=","files=",
                                                       "thermal_mode=","fps=","classes=", "text=", "add_date", 
                                                       "add_frame_id","stretch_frames"])
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
        elif opt in ["--add_frame_id"]:
            new_config["add_frame_id"] = True
        elif opt in ["--stretch_frames"]:
            new_config["stretch_frames"] = True
            
    make_video(**new_config)

if __name__ == "__main__":
   main(sys.argv[1:])
