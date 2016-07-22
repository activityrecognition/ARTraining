#!/bin/bash
#

###########################
#PEOPLE DETECTOR Vars

#true if it's required to download videos. false to use videos located in $videos_folder
donwload_videos=false

#path to folder where videos are saved or have to be saved
videos_folder=../videos_ipod5

#generate frames from videos
has_to_generate_frames=false

#thermix's group where videos are storaged
thermix_group=sarmiento_004

#thermix user email (videos will be downloaded from user's wall)
user_owner_email=ipod@ipod.com

#ccv model name
model_name=thermix_35a

#frames have to be stretched
stretch_frames=true

#frames need date
add_date=true

###########################
#POSES Vars
make_poses_video=true

#ccv model name
poses_model_name=thermix_33a

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

if [ $download_videos = true ]; then
python video_downloader.py -o $videos_folder -e $user_owner_email -l '[]' -g '["'"$thermix_group"'"]' -t '["14_tim"]' --incremental
fi

if [ $has_to_generate_frames = true ]; then
python prepare_data_for_training.py --all_labels="$all_labels" -l '["'"$thermix_group"'"]' -i $videos_folder -t '["14_tim"]' -o $frames_dir -m thermix_1 --remove_movement
else
python prepare_data_for_training.py --all_labels="$all_labels" -l '["'"$thermix_group"'"]' -t '["14_tim"]' -o $frames_dir -m thermix_1 --only_dataset
fi

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
input_dir=$frames_dir \
words_dir=$model_folder/"$model_name"._words \
results=$model_results_file \
stretch_image=$stretch_frames \
add_date=$add_date \
skip_if_file_exists=true \
runipy draw_cnn_on_images.ipynb
fi

python prepare_data_for_training.py --all_labels="$all_labels" -l '["'"$thermix_group"'"]' -t '["14_tim"]' -o $labeled_frames_path -m thermix_1 --only_dataset

#if [ ! -d ../mov_"$thermix_group"_"$model_name" ]; then
#python video_by_day_from_images.py -c '["3"]' -i $labeled_frames_path -t 14_tim -o ../mov_"$thermix_group"_"$model_name" -f #'["'"$labeled_frames_path"'/14_tim/thermix_1_files.txt"]' --split_in_days
#
#cd youtube_upload
#for filepath in $(ls -f ../../mov_"$thermix_group"_"$model_name"/*); do
#        video_name=$(basename "$filepath")
#        python upload_video.py --file=../../mov_"$thermix_group"_"$model_name"/$video_name \
#        --title="$thermix_group"_"$model_name"_"$video_name" --privacyStatus="private"
#done
#cd ..
#fi

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
  labeled_frames_path=/media/Gui2/thermix/"$model_name"_"$thermix_group"

#  if [ ! -d $labeled_frames_path ]; then
      output_dir=$labeled_frames_path \
      input_dir=$frames_dir \
      words_dir=$poses_model_folder/"$poses_model_name"._words \
      results=$poses_model_results_file \
      stretch_image=$stretch_frames \
      add_date=$add_date \
      skip_if_file_exists=false \
      runipy draw_cnn_on_images.ipynb
#  fi
  
#  python prepare_data_for_training.py --all_labels="$all_labels" -l '["'"$thermix_group"'"]' -t '["14_tim"]' -o $labeled_frames_path -m thermix_1 --only_dataset
  
  if [ ! -d ../mov_"$thermix_group"_"$poses_model_name" ]; then
      python video_by_day_from_images.py -c '["3"]' -i $labeled_frames_path -t 14_tim -o ../mov_"$thermix_group"_"$poses_model_name" -f '["'"$labeled_frames_path"'/14_tim/thermix_1_files.txt"]' --split_in_days

      cd youtube_upload
      for filepath in $(ls -f ../../mov_"$thermix_group"_"$poses_model_name"/*); do
        video_name=$(basename "$filepath")
        python upload_video.py --file=../../mov_"$thermix_group"_"$poses_model_name"/$video_name \
        --title="$thermix_group"_"$poses_model_name"_"$video_name" --privacyStatus="private"
      done

      cd ..
  fi
fi