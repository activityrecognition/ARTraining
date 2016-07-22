#PEOPLE DETECTOR Vars

#true if it's required to download videos. false to use videos located in $videos_folder
download_videos=true

#path to folder where videos are saved or have to be saved
#videos_folder=../videos_golden5s
videos_folder=$1

#generate frames from videos
has_to_generate_frames=true

#thermix's group where videos are storaged
#thermix_group=sarmiento_003
thermix_group=$2

#thermix user email (videos will be downloaded from user's wall)
#user_owner_email=golden5s@bramblexpress.com
user_owner_email=$3

#ccv model name
model_name=thermix_38a

#frames have to be stretched
stretch_frames=true

#frames need date
add_date=true

from_day=1
to_day=2

####################
#DO NOT MODIFY BELOW THIS LINE

#folder where raw frames without movement will be saved
frames_dir=/media/Gui2/thermix/"$thermix_group"_frames_no_movement

#folder where the ccv model is located
model_folder=/media/Gui2/thermix/ARTraining/trained_models/$model_name

#ccv model name
model_path=$model_folder/$model_name.sqlite3

#filepath that contains the cnn classification
model_results_file=$model_folder/"$thermix_group"_classify.txt

all_labels='["person","background","'"$thermix_group"'"]'

if [ $download_videos == true ]; then
python video_downloader.py -o $videos_folder -e $user_owner_email -l '[]' -g '["'"$thermix_group"'"]' -t '["14_tim"]' --incremental
fi

for day in `seq $from_day $to_day` ; do

echo day_"$day"

if [ $has_to_generate_frames == true ]; then
python prepare_data_for_training.py --all_labels="$all_labels" -l '["'"$thermix_group"'"]' -i $videos_folder -t '["14_tim"]' -o $frames_dir -m thermix_1 --remove_movement
fi

python prepare_data_for_training.py --all_labels="$all_labels" -l '["'"$thermix_group"'"]' -t '["14_tim"]' -o $frames_dir -m thermix_1 --only_dataset --day="$day"


if [ -f $model_results_file ]; then
    results_filepath=$model_results_file \
    dataset_filepath=$frames_dir/14_tim/thermix_1_files.txt \
    output_filepath=$frames_dir/14_tim/thermix_1_files.txt.temp \
    runipy get_non_classified_files.ipynb

    cd ../../ccv/bin
    ./cnnclassify $frames_dir/14_tim/thermix_1_files.txt.temp $model_path $frames_dir | tee -a $model_results_file
    
    rm -rf $frames_dir/14_tim/thermix_1_files.txt.temp
else
    cd ../../ccv/bin
    ./cnnclassify $frames_dir/14_tim/thermix_1_files.txt $model_path $frames_dir | tee $model_results_file
fi

cd ../../thermix/ARTraining
labeled_frames_path=/media/Gui2/thermix/"$model_name"_"$thermix_group"

if [ ! -d $labeled_frames_path ]; then
output_dir=$labeled_frames_path \
dataset_filepath=$frames_dir/14_tim/thermix_1_files.txt \
input_dir=$frames_dir \
words_dir=$model_folder/"$model_name"._words \
results=$model_results_file \
stretch_image=$stretch_frames \
add_date=$add_date \
skip_if_file_exists=true \
runipy draw_cnn_on_images.ipynb
fi

python prepare_data_for_training.py --all_labels="$all_labels" -l '["'"$thermix_group"'"]' -t '["14_tim"]' -o $labeled_frames_path -m thermix_1 --only_dataset

mov_dir=../mov_"$thermix_group"_"$model_name"_day"$day"
if [ ! -d $mov_dir ]; then
python video_by_day_from_images.py -c '["3"]' -i $labeled_frames_path -t 14_tim -o $mov_dir -f '["'"$labeled_frames_path"'/14_tim/thermix_1_files.txt"]'

cd youtube_upload
for filepath in $(ls -f ../$mov_dir/*); do
        video_name=$(basename "$filepath")
        python upload_video.py --file=../$mov_dir/$video_name \
        --title="$thermix_group"_"$model_name"_day"$day"_"$video_name" --privacyStatus="private"
done
cd ..

rm -rf $labeled_frames_path
fi

#generate graph
cnn_classification=$env_cnn_classification \
cnn_classnames=$env_cnn_classnames \
min_date=$env_min_date \
max_date=$env_max_date \
runipy plot_timelapse_cnn_results.ipynb

done