#!/usr/bin/env python
import requests, os, sys, getopt, ast, PIL, av, numpy, shutil
from PIL import Image, ImageFont, ImageDraw
from operator import itemgetter
from datetime import datetime, timedelta

FILE_DIR = os.path.abspath(os.path.dirname(__file__))

defaut_work_dir = "./trained_models/thermix_28b/classification_output"
default_thermal_mode = "4_tim"
default_file_paths = ["trained_models/thermix_28b/classification_output/4_tim/thermix_1_files.txt"]
default_output_dir = "../mov_suenos_dorados"
default_classes = ["3"]
default_fps = 60
default_text_to_draw = None
default_add_date = False
default_split_in_days = False

def create_temp_dir_for_video(video_path):
    temp_dir = os.path.splitext(video_path)[0] + "_temp"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    return temp_dir

def create_video_with_frames_in_path(frames_container, frame_rate, output_path):
    os.system("ffmpeg -framerate %d -pattern_type glob -i '%s/*.png' -c:v libx264 %s" % (frame_rate, 
                                                                                         frames_container, 
                                                                                         output_path))
    #cwd = os.getcwd()
    #os.system("cd %s && ffmpeg -r %d -f image2 -pattern_type glob -i '*.png' -vcodec libx264 %s && cd %s" % (frames_container,
    #                                                                                              frame_rate, 
    #                                                                                              output_path, cwd))
    shutil.rmtree(frames_container)
    
def make_video(wd=defaut_work_dir,
               tm=default_thermal_mode,
               filepaths=default_file_paths,
               od=default_output_dir,
               classes= default_classes,
               fps=default_fps,
               text_to_draw=default_text_to_draw,
               add_date=default_add_date,
               split_in_days=default_split_in_days):

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
            videos_sorted_by_date = sorted(videos_path.keys())
            for video in videos_sorted_by_date:
                video_frames = sorted(videos_path[video], key=itemgetter(0))
                for v in video_frames:
                    class_paths.append(os.path.join(video, "%s.%s" % v[1:]))
            # END Sort

            #if no video for this class, avoiding make a video without frames
            if len(videos_sorted_by_date) == 0:
                print "class %s empty" % c
                continue
                
            #array of couples with the format (start_date_of_day, end_date_of_day)
            days_ranges = []      
            
            #if split_in_days is not active, all frames will be added to the same video
            if split_in_days:
                #one video per day will be generated. 
                #the last day video will not be made unless it has more than 23hs 59m of frames
                
                end_date_of_day = None
                for video in videos_sorted_by_date:
                    name_of_video = os.path.basename(video)
                    
                    # str_date_of_video = 2016-06-20T18%3A46%3A22
                    str_date_of_video = "T".join(os.path.splitext(name_of_video)[0].split("_")[-2:])

                    # date_of_video = datetime(2016-06-20 18:46:22)
                    date_of_video = datetime.strptime(str_date_of_video,"%Y-%m-%dT%H%%3A%M%%3A%S")

                    #convert to argentinian date
                    date_of_video -= timedelta(hours=3)
                    
                    if not end_date_of_day or date_of_video > end_date_of_day:
                        date_of_video -= timedelta(seconds=date_of_video.second)
                        end_date_of_day = date_of_video + timedelta(hours=24)
                        days_ranges.append((date_of_video,end_date_of_day))
                
                #take out from list of videos to make the last day, if it doesn't have more than 23hs 59m of frames
                if days_ranges[-1][1] - date_of_video < timedelta(hours=23, minutes=59):
                    days_ranges = days_ranges[:-1]
                    
                if len(days_ranges) == 0:
                    print "class %s: for split_by_days option at least 1 full day is required" % c
                    continue
            
            output_paths=[]
            #outputs=[]
            #streams=[]
            #img = Image.open(class_paths[0])
            if split_in_days:
                for day_video in range(0, len(days_ranges)):  
                    output_path = os.path.join(output_dir, prefix_output+"_"+c+"_day_%03d"%(day_video+1)+".mp4")
                    
                    if os.path.exists(output_path):
                        print "%s already exists" % output_path
                        output_paths.append(None)
                        #outputs.append(None)
                        #streams.append(None)
                    else:
                        output_paths.append(output_path)
                        #outputs.append(av.open(output_paths[-1], 'w'))
                        #streams.append(outputs[-1].add_stream("mpeg4", "%d"%fps))
                        
                        #streams[-1].height = img.size[0]
                        #streams[-1].width = img.size[1]
            else:
                output_path = os.path.join(output_dir, prefix_output+"_"+c+".mp4")
                if os.path.exists(output_path):
                    print "%s already exists" % output_path
                    continue
                    
                output_paths.append(output_path)
                
                #outputs = [av.open(output_paths[0], 'w')]
                #streams = [outputs[0].add_stream("mpeg4", "%d" % fps)]

                #streams[0].height = img.size[0]
                #streams[0].width = img.size[1]

            index_of_day = 0
            temp_dir = None
            pending_frames_for_video = False
            i = 0
            for path in class_paths:
                # name_of_video = "Users_thermaldata_unkown_2016-06-20_18%3A46%3A22.000000_2"
                name_of_video = os.path.basename(os.path.dirname(path))

                # str_date_of_video = 2016-06-20T18%3A46%3A22
                str_date_of_video = "T".join(os.path.splitext(name_of_video)[0].split("_")[-2:])

                # date_of_video = datetime(2016-06-20 18:46:22)
                date_of_video = datetime.strptime(str_date_of_video,"%Y-%m-%dT%H%%3A%M%%3A%S")

                #convert to argentinian date
                date_of_video -= timedelta(hours=3)

                if split_in_days:
                    if not output_paths[index_of_day]:
                        index_of_day += 1
                        if index_of_day == len(days_ranges):
                            break
                        continue
                    if date_of_video < days_ranges[index_of_day][0]:
                        continue
                    elif date_of_video > days_ranges[index_of_day][1]:
                        assert(temp_dir)
                        
                        create_video_with_frames_in_path(temp_dir, fps, output_paths[index_of_day])
                        temp_dir = None
                        pending_frames_for_video = False
                        
                        index_of_day += 1
                        if index_of_day == len(days_ranges):
                            break

                #img = Image.open(path)

                #if img.mode != "RGB":
                #    img=img.convert("RGB")

                #if text_to_draw:
                #    draw = ImageDraw.Draw(img)
                #    font = ImageFont.truetype("SF-UI-Text-Medium.otf", 16)
                #    draw.text((10, 75),text_to_draw,(255,255,255),font=font)

                #if add_date:
                #    font = ImageFont.truetype("SF-UI-Text-Medium.otf", 12)
                #    draw = ImageDraw.Draw(img)
                #    draw.text((10, 200),date_of_video.strftime("%Y-%m-%d %H:%M"),(255,255,255),font=font)

                if not pending_frames_for_video:
                    temp_dir = create_temp_dir_for_video(output_paths[index_of_day])
                    pending_frames_for_video = True
                
                os.system("ln -s %s %s"%(path,os.path.join(temp_dir, 'img%020d.png'%i)))
                #img.save(os.path.join(temp_dir, 'img%020d.png'%i), 'png')
                i = i+1
                #img_matrix = numpy.asarray(img)#.reshape(img.size[0], img.size[1], 3)
                #frame = av.VideoFrame.from_ndarray(img_matrix)
                #packet = streams[index_of_day].encode(frame)
                #outputs[index_of_day].mux(packet)
            print i
            if pending_frames_for_video:
                create_video_with_frames_in_path(temp_dir, fps, output_paths[index_of_day])
                temp_dir = None
                pending_frames_for_video = False
            #if split_in_days:
            #    for day_video in range(0, len(days_ranges)):  
            #        if outputs[day_video]:
            #            outputs[day_video].close()
            #else:
            #    outputs[0].close()

def main(argv):
    new_config = {}
    try:
        opts, args = getopt.getopt(argv,"hi:o:f:t:c:",["help","input=","output=","files=",
                                                       "thermal_mode=","fps=","classes=", "text=", "add_date", "split_in_days"])
    except getopt.GetoptError:
        print """video_from_frames.py -i <input_dir> -o <output_dir> -f '["<file_with_image_paths1>",...]' """ + \
              """--fps=<fps> -t <x_tim> -c '["class1_id", ...]' --text=<text to draw in image> --add_date --split_in_days"""
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print """video_from_frames.py -i <input_dir> -o <output_dir> -f '["<file_with_image_paths1>",...]' """ + \
              """--fps=<fps> -t <x_tim> -c '["class1_id", ...]' --text=<text to draw in image> --add_date --split_in_days"""
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
        elif opt in ["--split_in_days"]:
            new_config["split_in_days"] = True

    make_video(**new_config)

if __name__ == "__main__":
    main(sys.argv[1:])
