#!/bin/bash

#groups="Victor_005 Victor_006 Charles_001 Charles_002 Julien_001 Luke_002 Irene_003 Julien_002 Charles_005 Anne_007"
groups="rgb_mapping"
tensorbox_input_json=../ARThermal/tensorbox_dataset_poses/tensorbox_input.json
tensorbox_video_path=../ARThermal/tensorbox_dataset_poses/tensorbox_input.mov
tensorbox_dataset=../ARThermal/tensorbox_dataset_poses

for group in $groups
do
    continue

    echo $group
    pedestrian=../ARThermal/"$group"_frames_no_movement/15_tim/sorted_frames_YOLO_results.txt

    if [ -f $pedestrian ]; then

        videos_location=../ARThermal/videos_ipod5
        if [ ! -d $videos_location/$group ]; then
            videos_location=../ARThermal/videos_black5
            if [ ! -d $videos_location/$group ]; then
                videos_location=../ARThermal/videos_golden5s
                if [ ! -d $videos_location/$group ]; then
                    videos_location=../ARThermal/videos_fede.polacov
                fi
            fi
        fi

        echo $videos_location
        
        videos_location=$videos_location group_name=$group tensorbox_input_filepath=$tensorbox_input_json tensorbox_dataset_dir=$tensorbox_dataset pedestrian_log_filepath=$pedestrian detector_type=yolo images_to_avoid_filepath=$tensorbox_dataset/images_to_avoid.txt runipy -o add_group_to_tensorbox_input.ipynb
    fi   
done

tensorbox_output_filepath=$tensorbox_video_path tensorbox_input_filepath=$tensorbox_input_json runipy make_tensorbox_video.ipynb

cd youtube_upload

video_name=tensorbox_input.mov
video_path=../$tensorbox_dataset/$video_name
python upload_video.py --file=$video_path \
        --title="$video_name" --privacyStatus="private"
        
cd ..