#!/bin/bash

#step 1: make frames for each group
video_folders="videos_golden5s videos_black5 videos_ipod5"
#video_folders="videos_black5"
output_dir=../ARThermal/public_dataset
for video_folder in $video_folders
do
    video_folder_path=../ARThermal/$video_folder
    for filepath in $(ls -f $video_folder_path/); do
        thermix_group=$(basename "$filepath")
        
        all_labels='["person","background","'"$thermix_group"'"]'
        
        if [ "$thermix_group" == "suenos_dorados_5" ] || [ "$thermix_group" == "." ] || \
        [ "$thermix_group" == ".." ] || [ "$thermix_group" == "Marge_001" ] || [ "$thermix_group" == "Marge_003" ] || \
        [ "$thermix_group" == "Marge_004" ] || \
        [ "$thermix_group" == "Anne_001" ] || [ "$thermix_group" == "Anne_002" ] || [ "$thermix_group" == "Anne_003" ] || \
        [ "$thermix_group" == "Anne_004" ]; then
            continue
        fi
        
        if [ ! -d  $video_folder_path/$thermix_group ]; then
            continue
        fi
        
        echo $thermix_group
        
        size_param="--no_resize"
        if [ $video_folder == "videos_black5" ]; then
            size_param='--crop_frames_to_rect=(0,0,120,160)'
        fi
        
        if [ ! -d $output_dir/$thermix_group ]; then
        python prepare_data_for_training.py --all_labels="$all_labels" -l '["'"$thermix_group"'"]' -i $video_folder_path -t '["14_tim"]' -o $output_dir/$thermix_group -m thermix_1 --remove_movement $size_param --use_frame_id
          
        ./ccv_classify_for_public_dataset.sh $thermix_group
        
        #copy annotations
        \cp trained_models/thermix_42a/$thermix_group"_annotations.txt" $output_dir/$thermix_group
        fi
    done
done

#step 2: organize files structure
#modify annotations paths and rename video folders
runipy organize_public_dataset.ipynb

#remove old structure
for filepath in $(ls $output_dir/); do
        thermix_group=$(basename "$filepath")
        echo "$thermix_group"
        has_files=$(ls $output_dir/$thermix_group/14_tim/3 | wc -l)
        if [ "$has_files" == "0"]; then
            echo "All files moved"
            #rm -rf $output_dir/$thermix_group/14_tim
        fi
done