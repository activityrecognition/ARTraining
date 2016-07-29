#PEOPLE DETECTOR Vars

#true if it's required to download videos. false to use videos located in $videos_folder
donwload_videos=false

#path to folder where videos are saved or have to be saved
videos_folder=../ARThermal/videos_golden5s

#generate frames from videos
has_to_generate_frames=false

#thermix's group where videos are storaged
thermix_group=$1 #full_day_pedro

#thermix user email (videos will be downloaded from user's wall)
user_owner_email=golden5s@bramblexpress.com

#ccv model name
model_name=thermix_35a

#frames have to be stretched
stretch_frames=true

#frames need date
add_date=true

from_day=$2
to_day=$3

###########################
#POSES Vars
make_poses_video=true

#ccv model name
poses_model_name=thermix_33a

####################
#DO NOT MODIFY BELOW THIS LINE

#folder where raw frames without movement will be saved
frames_dir=/media/Gui2/thermix/ARThermal/"$thermix_group"_frames_no_movement

#folder where the ccv model is located
model_folder=/media/Gui2/thermix/ARTraining/trained_models/$model_name

#ccv model name
model_path=$model_folder/$model_name.sqlite3

#filepath that contains the cnn classification
model_results_file=$model_folder/"$thermix_group"_classify.txt

all_labels='["person","background","'"$thermix_group"'"]'

if [ $download_videos = true ]; then
python video_downloader.py -o $videos_folder -e $user_owner_email -l '[]' -g '["'"$thermix_group"'"]' -t '["14_tim"]' --incremental
fi

for day in `seq $from_day $to_day` ; do

echo day_"$day"

if [ $has_to_generate_frames = true ]; then
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
labeled_frames_path=../ARThermal/"$model_name"_"$thermix_group"_day"$day"

#if [ ! -d $labeled_frames_path ]; then
output_dir=$labeled_frames_path \
dataset_filepath=$frames_dir/14_tim/thermix_1_files.txt \
input_dir=$frames_dir \
words_dir=$model_folder/"$model_name"._words \
results=$model_results_file \
stretch_image=$stretch_frames \
add_date=$add_date \
skip_if_file_exists=true \
skip_labels='["person"]' \
add_frame_id=true \
runipy draw_cnn_on_images.ipynb
#fi

python prepare_data_for_training.py --all_labels="$all_labels" -l '["'"$thermix_group"'"]' -t '["14_tim"]' -o $labeled_frames_path -m thermix_1 --only_dataset

if [ $make_poses_video = true ]; then
  #folder where the ccv model is located
  poses_model_folder=/media/Gui2/thermix/ARTraining/trained_models/$poses_model_name

  #ccv model name
  poses_model_path=$poses_model_folder/$poses_model_name.sqlite3

  #filepath that contains the cnn classification
  poses_model_results_file=$poses_model_folder/"$thermix_group"_poses_classify.txt 

  output_filepath=$frames_dir/14_tim/thermix_1_files_poses.txt \
  input_dir=$frames_dir \
  words_dir=$model_folder/"$model_name"._words \
  results=$model_results_file \
  runipy select_person_frames.ipynb
  
  if [ -f $poses_model_results_file ]; then
    results_filepath=$poses_model_results_file \
    dataset_filepath=$frames_dir/14_tim/thermix_1_files_poses.txt \
    output_filepath=$frames_dir/14_tim/thermix_1_files_poses.txt.temp \
    runipy get_non_classified_files.ipynb

    cd ../../ccv/bin
    ./cnnclassify $frames_dir/14_tim/thermix_1_files_poses.txt.temp $poses_model_path $frames_dir | tee -a $poses_model_results_file
    
    rm -rf $frames_dir/14_tim/thermix_1_files_poses.txt.temp
  else
    cd ../../ccv/bin
    ./cnnclassify $frames_dir/14_tim/thermix_1_files_poses.txt $poses_model_path $frames_dir | tee $poses_model_results_file
  fi
  
  cd ../../thermix/ARTraining
  labeled_frames_path=../ARThermal/"$model_name"_"$thermix_group"_day"$day"

#  if [ ! -d $labeled_frames_path ]; then
      output_dir=$labeled_frames_path \
      dataset_filepath=$frames_dir/14_tim/thermix_1_files.txt \
      input_dir=$frames_dir \
      words_dir=$poses_model_folder/"$poses_model_name"._words \
      results=$poses_model_results_file \
      stretch_image=$stretch_frames \
      add_date=$add_date \
      skip_if_file_exists=true \
      add_frame_id=true \
      runipy draw_cnn_on_images.ipynb
#  fi
  
python prepare_data_for_training.py --all_labels="$all_labels" -l '["'"$thermix_group"'"]' -t '["14_tim"]' -o $labeled_frames_path -m thermix_1 --only_dataset

fi

mov_dir=../mov_"$thermix_group"_"$model_name"_day"$day"
if [ ! -d $mov_dir ]; then
python video_by_day_from_images.py -c '["3"]' -i $labeled_frames_path -t 14_tim -o $mov_dir -f '["'"$labeled_frames_path"'/14_tim/thermix_1_files.txt"]'
fi
cd youtube_upload
for filepath in $(ls -f ../$mov_dir/*); do
        video_name=$(basename "$filepath")
        python upload_video.py --file=../$mov_dir/$video_name \
        --title="$thermix_group"_"$model_name"_day"$day"_"$video_name" --privacyStatus="private"
done
cd ..

#rm -rf $labeled_frames_path
#fi

done
