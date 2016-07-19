#!/usr/bin/env python

#required:
## Mac:
### brew install ffmpeg pkg-config
## Ubuntu:
###sudo apt-get -y install build-essential checkinstall git libfaac-dev libgpac-dev \
###libmp3lame-dev libopencore-amrnb-dev libopencore-amrwb-dev libtheora-dev \
###libvorbis-dev pkg-config texi2html yasm zlib1g-dev libasound-dev
###wget http://ffmpeg.org/releases/ffmpeg-2.7.tar.bz2
###tar -xjf ffmpeg-2.7.tar.bz2
###cd ffmpeg-2.7
###
###./configure --disable-static --enable-shared --disable-doc
###make
###sudo make install
## All:
###pip install av
import os, getopt, sys, shutil, av, ast, random
import PIL

FILE_DIR = os.path.abspath(os.path.dirname(__file__))

#each group has a folder inside input_dir
default_input_dir = os.path.join(FILE_DIR,"../videos")

default_output_dir = os.path.join(FILE_DIR,"dataset")

default_labels = ["people", "background", "full_day"]

default_model_name = "thermix_1"

default_thermal_image_modes = ["4_tim"]

default_labels_for_dataset = ["people", "background"]

default_training_proportion = 0.80
default_testing_proportion = 1-default_training_proportion

def label_for_group(group_name, labels):
    group_label = [item for item in labels if item in group_name]
    if len(group_label) != 1:
        return None
    return group_label[0]

def create_dataset_folders(dataset_dir, all_labels, dataset_labels):
    for label in dataset_labels:
        path_for_label = os.path.join(dataset_dir, str(all_labels.index(label)+1))
        if not os.path.exists(path_for_label):
            os.makedirs(path_for_label)

def save_frames_of_video(video_path, one_image_per_channel=False):
    try:
        container = av.open(video_path)
        video = next(s for s in container.streams if s.type == b'video')

        for packet in container.demux(video):
            for frame in packet.decode():
                img = frame.to_image()
                img = img.resize((257, 257))
                if one_image_per_channel:
                    rgb = img.split()
                    for i,channel in enumerate(rgb):
                        frame_path = os.path.join(os.path.dirname(video_path),'%d_%d.png' % (frame.index,i))
                        if os.path.exists(frame_path):
                            return
                        img2 = PIL.Image.merge("RGB", (channel, channel, channel))
                        img2.save(frame_path)
                else:
                    frame_path = os.path.join(os.path.dirname(video_path),'%d.png' % frame.index)
                    if os.path.exists(frame_path):
                        return
                    img.save(frame_path)
                    
        return True
    except Exception as e:
        print e
        print "Error getting frames of video %s" % video_path
        return False

def generate_training_and_testing_list(output_dir=default_output_dir,
                                       model_name=default_model_name,
                                       training_proportion=default_training_proportion,
                                       testing_proportion=default_testing_proportion,
                                       thermal_image_modes=default_thermal_image_modes,
                                       all_labels=default_labels,
                                       labels_for_dataset=default_labels_for_dataset):
    list_of_thermal_folders = os.listdir(output_dir)

    for thermal_folder in list_of_thermal_folders:
        if thermal_folder not in thermal_image_modes:
            continue

        base_dir = os.path.join(output_dir,thermal_folder)

        categories = os.listdir(base_dir)

        # file_list = [cat_1, cat_2, ...]
        # cat_n = [mov_1, mov_2, ...]
        # mov_n = [frame_1, frame_2, ...]
        file_list = []
        with open(os.path.join(base_dir,"%s_files.txt" % model_name), "wb") as handle:
            for category in categories:
                category_dir = os.path.join(base_dir, category)
                if not os.path.isdir(category_dir):
                    continue

                try:
                    if all_labels[int(category)-1] not in labels_for_dataset:
                        continue
                except Exception as e:
                    continue

                cat = []
                file_list.append((category,cat))
                category_videos = os.listdir(category_dir)
                for video in category_videos:
                    video_dir = os.path.join(category_dir, video)
                    if not os.path.isdir(video_dir):
                        continue

                    mov = []
                    cat.append(mov)
                    frames = os.listdir(video_dir)
                    for frame in frames:
                        frame_path = os.path.join(thermal_folder, category, video, frame)
                        mov.append("%s %s " % (category, frame_path))

                        #write _files.txt
                        handle.write("%s %s \n" % (category, frame_path))

	max_dataset_len = 0
        cat_lens = []
	for _,cat in file_list:
	   cat_lens.append(sum([len(i) for i in cat]))
	max_dataset_len = sorted(cat_lens)[0]
	print "max training dataset count: %d"%max_dataset_len
	#prom /= len(file_list)
  
        testing_frames = []
        training_frames = []
        print  thermal_folder
        for cat_name,cat in file_list:
            total_number_of_frames = sum([len(i) for i in cat])
            testing_number_of_frames = max_dataset_len*testing_proportion
            cat_testing_frames = []
            while len(cat_testing_frames) < testing_number_of_frames:
                mov = random.choice(cat)
                cat.remove(mov)
                cat_testing_frames.extend(mov)

            percentage = len(cat_testing_frames)/float(max_dataset_len)*100
            print "* category %s: \n** total_frames= %d\n** testing_frames= %d (%.2f%%)" % \
                  (cat_name, total_number_of_frames, len(cat_testing_frames),percentage)
            testing_frames.extend(cat_testing_frames)

            while sum([len(i) for i in cat]) > max_dataset_len*training_proportion:
		mov =random.choice(cat)
		if len(mov) > 0:
		    mov.remove(random.choice(mov))

            for mov in cat:
                training_frames.extend(mov)
	    print "** training_frames= %d" %sum([len(i) for i in cat])
        random.shuffle(training_frames)
        with open(os.path.join(base_dir,"%s_training.txt" % model_name), "wb") as handle:
            for f in training_frames:
                handle.write("%s \n"%f)

        random.shuffle(testing_frames)
        with open(os.path.join(base_dir,"%s_testing.txt" % model_name), "wb") as handle:
            for f in testing_frames:
                handle.write("%s \n"%f)

        total_frames_count = len(training_frames)+len(testing_frames)
        print "***************"
        print "total number of frames: %d\ntotal training frames: %d (%.2f%%)\n** total testing frames: %d (%.2f%%)" % \
                (total_frames_count, len(training_frames), len(training_frames)/float(total_frames_count)*100,
                 len(testing_frames), len(testing_frames)/float(total_frames_count)*100)
        print "***************"

        with open(os.path.join(base_dir,"%s_links.txt" % model_name), "wb") as handle:
            for label in labels_for_dataset:
                handle.write("%d %s \n" % (all_labels.index(label)+1,label))

        with open(os.path.join(base_dir,"%s._words" % model_name), "wb") as handle:
            for label in labels_for_dataset:
                handle.write("%s \n" % label)

def prepare_dataset_for_training(input_dir=default_input_dir, output_dir=default_output_dir,
                                 all_labels=default_labels, model_name=default_model_name,
                                 training_proportion=default_training_proportion,
                                 testing_proportion=default_testing_proportion,
                                 thermal_image_modes=default_thermal_image_modes,
                                 labels_for_dataset=default_labels_for_dataset, 
                                 remove_movement=False):
    if len(labels_for_dataset) == 0:
        raise "At least one label is required"

    for label in labels_for_dataset:
        if label not in all_labels:
            raise "all labels_for_dataset must be included in all_labels"

    if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    groups_dirs = os.listdir(input_dir)

    print groups_dirs
    for group_dir in groups_dirs:
        group_label = label_for_group(group_dir,labels_for_dataset)
        if not group_label:
            continue

        print "Processing group %s in label %s" % (group_dir, group_label)

        group_path = os.path.join(input_dir,group_dir)
        thermal_dirs = os.listdir(group_path)

        for thermal_dir in thermal_dirs:
            if thermal_dir not in thermal_image_modes:
                continue

            output_thermal = os.path.join(output_dir, thermal_dir)
            if not os.path.exists(output_thermal):
                os.makedirs(output_thermal)

            create_dataset_folders(output_thermal, all_labels, labels_for_dataset)

            thermal_path = os.path.join(group_path, thermal_dir)
            if not os.path.isdir(thermal_path):
                continue
            input_thermal_files = os.listdir(thermal_path)

            for file in input_thermal_files:
                print "Generating frames of file %s" % file
                destination_dir = os.path.join(output_thermal,str(all_labels.index(group_label)+1),os.path.splitext(file)[0])
                if not os.path.exists(destination_dir):
                    os.makedirs(destination_dir)

                src = os.path.join(thermal_path,file)
                dest = os.path.join(destination_dir, file)
                shutil.copyfile(src, dest)
                save_frames_of_video(dest, remove_movement)
                os.remove(dest)

    generate_training_and_testing_list(output_dir, model_name, training_proportion, testing_proportion,
                                       thermal_image_modes, all_labels, labels_for_dataset)

def main(argv):
    new_config = {}
    only_dataset = False
    try:
        opts, args = getopt.getopt(argv,"hi:o:l:m:p:t:",["help","input=","output=","labels=","model_name=",
                                                         "testing_proportion=","only_dataset", "thermal_modes=", "remove_movement"])
    except getopt.GetoptError:
        print """prepare_data_for_training.py -i <inputDir> -o <outputDir> -l '["<label1>","<label2>"]' """+ \
              """-m <model_name> -p <testing_proportion> -t '["4_tim","14_tim"]' --remove_movement --only_dataset"""
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print """prepare_data_for_training.py -i <inputDir> -o <outputDir> -l '["<label1>","<label2>"]' """+ \
              """-m <model_name> -p <testing_proportion> -t '["4_tim","14_tim"]' --remove_movement --only_dataset"""
            sys.exit()
        elif opt in ("-o", "--output"):
            new_config["output_dir"] = arg
        elif opt in ("-i", "--input"):
            new_config["input_dir"] = arg
        elif opt in ("-m", "--model_name"):
            new_config["model_name"] = arg
        elif opt in ("-p", "--testing_proportion"):
            new_config["testing_proportion"] = float(arg)
            new_config["training_proportion"] = 1.0-float(arg)
        elif opt in ("-l", "--labels"):
            new_config["labels_for_dataset"] = ast.literal_eval("%s" % arg)
        elif opt in ("-t", "--thermal_modes"):
            new_config["thermal_image_modes"] = ast.literal_eval("%s" % arg)
        elif opt in ("--remove_movement"):
            new_config["remove_movement"] = True
        elif opt in ("--only_dataset"):
            only_dataset = True

    if only_dataset:
        new_config.pop("remove_movement",False)
        new_config.pop("input_dir",None)
        generate_training_and_testing_list(**new_config)
    else:
        prepare_dataset_for_training(**new_config)

if __name__ == "__main__":
   main(sys.argv[1:])
