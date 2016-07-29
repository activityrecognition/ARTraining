#!/bin/bash

model_name=thermix_38a

#folder where the ccv model is located
model_folder=/media/Gui2/thermix/ARTraining/trained_models/$model_name

#ccv model name
model_path=$model_folder/$model_name.sqlite3

#download all groups of user golden5s
user_owner_email=golden5s@bramblexpress.com
videos_folder=../ARThermal/videos_golden5s

##################################################################
##################################################################
thermix_group=sarmiento_003
frames_dir=../ARThermal/"$thermix_group"_frames_no_movement
mov_dir=../mov_"$thermix_group"_all_frames
all_labels='["person","background","'"$thermix_group"'"]'

#python video_downloader.py -o $videos_folder -e $user_owner_email -l '[]' -g '["'"$thermix_group"'"]' -t '["14_tim"]' --incremental

#python prepare_data_for_training.py --all_labels="$all_labels" -l '["'"$thermix_group"'"]' -i $videos_folder -t '["14_tim"]' -o $frames_dir -m thermix_1 --remove_movement

#if [ ! -d $mov_dir ]; then
#python video_from_images.py -c '["3"]' -i $frames_dir -t 14_tim -o $mov_dir -f '["'"$frames_dir"'/14_tim/thermix_1_files.txt"]' --add_date --stretch_frames --add_frame_id

#cd youtube_upload
#for filepath in $(ls -f ../$mov_dir/*); do
#        video_name=$(basename "$filepath")
#        python upload_video.py --file=../$mov_dir/$video_name \
#        --title="$thermix_group"_"$model_name"_day"$day"_"$video_name" --privacyStatus="private"
#done
#cd ..
#fi

##################################################################
##################################################################
thermix_group=sarmiento_005
frames_dir=../ARThermal/"$thermix_group"_frames_no_movement
mov_dir=../mov_"$thermix_group"_all_frames
all_labels='["person","background","'"$thermix_group"'"]'

#python video_downloader.py -o $videos_folder -e $user_owner_email -l '[]' -g '["'"$thermix_group"'"]' -t '["14_tim"]' --incremental

#python prepare_data_for_training.py --all_labels="$all_labels" -l '["'"$thermix_group"'"]' -i $videos_folder -t '["14_tim"]' -o $frames_dir -m thermix_1 --remove_movement

#if [ ! -d $mov_dir ]; then
#python video_from_images.py -c '["3"]' -i $frames_dir -t 14_tim -o $mov_dir -f '["'"$frames_dir"'/14_tim/thermix_1_files.txt"]' --add_date --stretch_frames --add_frame_id

#cd youtube_upload
#for filepath in $(ls -f ../$mov_dir/*); do
#        video_name=$(basename "$filepath")
#        python upload_video.py --file=../$mov_dir/$video_name \
#        --title="$thermix_group"_"$model_name"_day"$day"_"$video_name" --privacyStatus="private"
#done
#cd ..
#fi

##################################################################
##################################################################
thermix_group=sarmiento_007
frames_dir=../ARThermal/"$thermix_group"_frames_no_movement
mov_dir=../mov_"$thermix_group"_all_frames
all_labels='["person","background","'"$thermix_group"'"]'

#python video_downloader.py -o $videos_folder -e $user_owner_email -l '[]' -g '["'"$thermix_group"'"]' -t '["14_tim"]' --incremental

#python prepare_data_for_training.py --all_labels="$all_labels" -l '["'"$thermix_group"'"]' -i $videos_folder -t '["14_tim"]' -o $frames_dir -m thermix_1 --remove_movement

if [ ! -d $mov_dir ]; then
python video_from_images.py -c '["3"]' -i $frames_dir -t 14_tim -o $mov_dir -f '["'"$frames_dir"'/14_tim/thermix_1_files.txt"]' --add_date --stretch_frames --add_frame_id

cd youtube_upload
for filepath in $(ls -f ../$mov_dir/*); do
        video_name=$(basename "$filepath")
        python upload_video.py --file=../$mov_dir/$video_name \
        --title="$thermix_group"_"$model_name"_day"$day"_"$video_name" --privacyStatus="private"
done
cd ..
fi

#download all groups of user ipod5
user_owner_email=ipod@ipod.com
videos_folder=../ARThermal/videos_ipod5

##################################################################
##################################################################
thermix_group=sarmiento_004
frames_dir=../ARThermal/"$thermix_group"_frames_no_movement
mov_dir=../mov_"$thermix_group"_all_frames
all_labels='["person","background","'"$thermix_group"'"]'

#python video_downloader.py -o $videos_folder -e $user_owner_email -l '[]' -g '["'"$thermix_group"'"]' -t '["14_tim"]' --incremental

#python prepare_data_for_training.py --all_labels="$all_labels" -l '["'"$thermix_group"'"]' -i $videos_folder -t '["14_tim"]' -o $frames_dir -m thermix_1 --remove_movement

#if [ ! -d $mov_dir ]; then
#python video_from_images.py -c '["3"]' -i $frames_dir -t 14_tim -o $mov_dir -f '["'"$frames_dir"'/14_tim/thermix_1_files.txt"]' --add_date --stretch_frames --add_frame_id

#cd youtube_upload
#for filepath in $(ls -f ../$mov_dir/*); do
#        video_name=$(basename "$filepath")
#        python upload_video.py --file=../$mov_dir/$video_name \
#        --title="$thermix_group"_"$model_name"_day"$day"_"$video_name" --privacyStatus="private"
#done
#cd ..
#fi

##################################################################
##################################################################
thermix_group=sarmiento_006
frames_dir=../ARThermal/"$thermix_group"_frames_no_movement
mov_dir=../mov_"$thermix_group"_all_frames
all_labels='["person","background","'"$thermix_group"'"]'

#python video_downloader.py -o $videos_folder -e $user_owner_email -l '[]' -g '["'"$thermix_group"'"]' -t '["14_tim"]' --incremental

#python prepare_data_for_training.py --all_labels="$all_labels" -l '["'"$thermix_group"'"]' -i $videos_folder -t '["14_tim"]' -o $frames_dir -m thermix_1 --remove_movement

#if [ ! -d $mov_dir ]; then
#python video_from_images.py -c '["3"]' -i $frames_dir -t 14_tim -o $mov_dir -f '["'"$frames_dir"'/14_tim/thermix_1_files.txt"]' --add_date --stretch_frames --add_frame_id

#cd youtube_upload
#for filepath in $(ls -f ../$mov_dir/*); do
#        video_name=$(basename "$filepath")
#        python upload_video.py --file=../$mov_dir/$video_name \
#        --title="$thermix_group"_"$model_name"_day"$day"_"$video_name" --privacyStatus="private"
#done
#cd ..
#fi

##################################################################
##################################################################
thermix_group=sarmiento_008
frames_dir=../ARThermal/"$thermix_group"_frames_no_movement
mov_dir=../mov_"$thermix_group"_all_frames
all_labels='["person","background","'"$thermix_group"'"]'

#python video_downloader.py -o $videos_folder -e $user_owner_email -l '[]' -g '["'"$thermix_group"'"]' -t '["14_tim"]' --incremental

#python prepare_data_for_training.py --all_labels="$all_labels" -l '["'"$thermix_group"'"]' -i $videos_folder -t '["14_tim"]' -o $frames_dir -m thermix_1 --remove_movement

if [ ! -d $mov_dir ]; then
python video_from_images.py -c '["3"]' -i $frames_dir -t 14_tim -o $mov_dir -f '["'"$frames_dir"'/14_tim/thermix_1_files.txt"]' --add_date --stretch_frames --add_frame_id

cd youtube_upload
for filepath in $(ls -f ../$mov_dir/*); do
        video_name=$(basename "$filepath")
        python upload_video.py --file=../$mov_dir/$video_name \
        --title="$thermix_group"_"$model_name"_day"$day"_"$video_name" --privacyStatus="private"
done
cd ..
fi