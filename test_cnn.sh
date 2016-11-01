#./test_cnn.sh ../ARThermal/videos_pablo.pusiol debug pp@pp.com 1 1 true true '["14_tim"]'
#./test_cnn.sh ../ARThermal/videos_fede.polacov fede_debug fpolacov@gmail.com 1 1 true true '["14_tim"]'
#PEOPLE DETECTOR Vars

#true if it's required to download videos. false to use videos located in $videos_folder
download_videos=$6

#path to folder where videos are saved or have to be saved
#videos_folder=../videos_golden5s
videos_folder=$1

#generate frames from videos
has_to_generate_frames=$7

#thermix's group where videos are storaged
#thermix_group=sarmiento_003
thermix_group=$2

#tim='["'14_tim'"]'
#tim=$8
thermal_tim=14_tim

#thermix user email (videos will be downloaded from user's wall)
#user_owner_email=golden5s@bramblexpress.com
user_owner_email=$3

#ccv model name
model_name=thermix_42a

#frames have to be stretched
stretch_frames=true

#frames need date
add_date=true

add_frame_id=true

from_day=$4
to_day=$5

####################
#DO NOT MODIFY BELOW THIS LINE

#folder where raw frames without movement will be saved
frames_dir=/workspace/thermix/ARThermal/"$thermix_group"_no_resized

#folder where the ccv model is located
model_folder=/workspace/thermix/ARTraining/trained_models/$model_name

#ccv model name
model_path=$model_folder/$model_name.sqlite3

#filepath that contains the cnn classification
model_results_file=$model_folder/"$thermix_group"_classify.txt

all_labels='["person","background","'"$thermix_group"'"]'

if [ $download_videos == true ]; then
python video_downloader.py -o $videos_folder -e $user_owner_email -l '[]' -g '["'"$thermix_group"'"]' -t '["'"$thermal_tim"'"]' --incremental
fi

if [ $has_to_generate_frames == true ]; then

videos_folder_name=$(basename "$videos_folder")
size_param="--no_resize"
if [ $videos_folder_name == "videos_black5" ]; then
    size_param='--crop_frames_to_rect=(0,0,120,160)'
fi
        
python prepare_data_for_training.py --all_labels="$all_labels" -l '["'"$thermix_group"'"]' -i $videos_folder -t '["'"$thermal_tim"'"]' -o $frames_dir -m thermix_1 --remove_movement $size_param
fi

#cd ../../ccv/bin
#./cnnclassify $frames_dir/$thermal_tim/thermix_1_files.txt $model_path $frames_dir | tee $model_results_file