#!/bin/bash

#Script tasks:
#  download rgb videos
#  create frames 
#  list them in a file excluding black frames

group_name=$1
email=$3
#email=ipod@ipod.com
output_videos=$2

#for downloading videos
python video_downloader_direct.py -e $email -g '["'"$group_name"'"]' -t '["15_tim"]' -o $output_videos -l '[]' --incremental

#for generating frames
python prepare_data_for_training.py --all_labels='["person","background","'"$group_name"'"]' -l '["'"$group_name"'"]' -i $output_videos -t '["15_tim"]' -o ../ARThermal/"$group_name"_frames_no_movement -m thermix_1 --no_resize

sorted_frame_list=../ARThermal/"$group_name"_frames_no_movement/15_tim/sorted_frames.txt

# list frame paths in a file excluding black frames
output_file="$sorted_frame_list" \
dataset_dir=../ARThermal/"$group_name"_frames_no_movement \
tim=15_tim \
category=3 \
runipy get_sorted_list_of_frames.ipynb

exit

#From here, historic code for processing frames using icf pedestrian detector

output_frames_path=/media/Gui2/thermix/ARThermal/"$group_name"_frames_pedestrian/15_tim/3

mkdir -p $output_frames_path

cd ../../ccv/bin/

n=1
ext='.png'
while IFS='' read -r line || [[ -n "$line" ]]; do
 output_image_path="$output_frames_path"/"$(printf %020d $n)"${ext}
 ./icfdetect $line ../samples/pedestrian.icf | ./icfdraw.rb $line $output_image_path
 echo "$output_image_path"
 echo "$line"
 n=$(( $n + 1 ))
done < "$sorted_frame_list" | tee ../../thermix/ARTraining/log_"$group_name"_pedestrian.log

cd ../../thermix/ARTraining

echo $(cat log_pedestrian.log | grep "total : 1" | wc -l)

video_name="$group_name"_pedestrian.mp4
video_path=$output_frames_path/../$video_name

current_path=$(pwd)

cd $output_frames_path
ffmpeg -framerate 60 -pattern_type glob -i './*.png' -c:v libx264 $video_path
cd $current_path

cd youtube_upload

python upload_video.py --file=$video_path \
        --title="$video_name" --privacyStatus="private"
        
cd ..