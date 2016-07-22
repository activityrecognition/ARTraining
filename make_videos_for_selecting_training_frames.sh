#PEOPLE DETECTOR Vars

#true if it's required to download videos. false to use videos located in $videos_folder
donwload_videos=false

#path to folder where videos are saved or have to be saved
videos_folder=../videos_golden5s

#generate frames from videos
has_to_generate_frames=false

#thermix's group where videos are storaged
thermix_group=sarmiento_003

#thermix user email (videos will be downloaded from user's wall)
user_owner_email=golden5s@bramblexpress.com

#ccv model name
model_name=thermix_38a

#frames have to be stretched
stretch_frames=true

#frames need date
add_date=true

from_day=1
to_day=1

####################
#DO NOT MODIFY BELOW THIS LINE

#folder where raw frames without movement will be saved
frames_dir=../"$thermix_group"_frames_no_movement

#folder where the ccv model is located
model_folder=./trained_models/$model_name

#ccv model name
model_path=$model_folder/$model_name.sqlite3

#filepath that contains the cnn classification
model_results_file=$model_folder/"$thermix_group"_classify.txt

all_labels='["person","background","'"$thermix_group"'"]'

for day in `seq $from_day $to_day` ; do

echo day_"$day"

python prepare_data_for_training.py --all_labels="$all_labels" -l '["'"$thermix_group"'"]' -t '["14_tim"]' -o $frames_dir -m for_training_day_"$day" --only_dataset --day="$day"

mov_dir=../mov_"$thermix_group"_for_training_day"$day"
if [ ! -d $mov_dir ]; then
python video_from_images.py -c '["3"]' -i $frames_dir -t 14_tim -o $mov_dir -f '["'"$frames_dir"'/14_tim/for_training_day_'"$day"'_files.txt"]' --add_frame_id --stretch_frames

cd youtube_upload
for filepath in $(ls -f ../$mov_dir/*); do
        video_name=$(basename "$filepath")
        python upload_video.py --file=../$mov_dir/$video_name \
        --title="$thermix_group"_"$video_name" --privacyStatus="private"
done
cd ..
fi

done