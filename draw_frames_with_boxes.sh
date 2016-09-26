#thermix's group where videos are storaged
thermix_group=$1

thermal_tim=14_tim

####################
#DO NOT MODIFY BELOW THIS LINE

folder where frame are storaged
frames_dir=/media/Gui2/thermix/ARThermal/"$thermix_group"_frames_with_boxes

all_labels='["person","background","'"$thermix_group"'"]'

python prepare_data_for_training.py --all_labels="$all_labels" -l '["'"$thermix_group"'"]' -t '["'"$thermal_tim"'"]' -o $frames_dir -m thermix_1 --only_dataset

mov_dir=../mov_"$thermix_group"_with_boxes
#if [ ! -d $mov_dir ]; then
python video_by_day_from_images.py -c '["3"]' -i $frames_dir -t $thermal_tim -o $mov_dir -f '["'"$frames_dir"'/'"$thermal_tim"'/thermix_1_files.txt"]' --fps=30

cd youtube_upload
for filepath in $(ls -f ../$mov_dir/*); do
        video_name=$(basename "$filepath")
        python upload_video.py --privacyStatus="private" --file=../$mov_dir/$video_name \
        --title="$video_name"
done
cd ..

#fi

#frames_dir=/media/Gui2/thermix/ARThermal/"$thermix_group"

#all_labels='["lying","sitting","standing","people","background"]'

#python prepare_data_for_training.py --all_labels="$all_labels" -l "$all_labels" -t '["'"$thermal_tim"'"]' -o $frames_dir -m thermix_1 --only_dataset

#mov_dir=../mov_"$thermix_group"_with_boxes
#if [ ! -d $mov_dir ]; then
#python video_from_images.py -c '["2","3"]' -i $frames_dir -t $thermal_tim -o $mov_dir -f '["'"$frames_dir"'/'"$thermal_tim"'/thermix_1_files.txt"]' --fps=1 --add_frame_id

#cd youtube_upload
#for filepath in $(ls -f ../$mov_dir/*); do
#        video_name=$(basename "$filepath")
#        python upload_video.py --privacyStatus="private" --file=../$mov_dir/$video_name \
#        --title="$video_name"
#done
#cd ..

#fi