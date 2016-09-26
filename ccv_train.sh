#!/bin/sh
#

if [ $# -lt 1 ]; then
    echo $0: usage: train.sh model_name
    exit 1
fi

model_name=$1

tim=14_tim

dataset_bucket=../dataset_bucket

full_dataset=../dataset_merged

acted_dataset=../dataset_poses_people_background

all_labels='["lying","sitting","standing","people","background"]'

videos_bucket_folder=../ARThermal/videos_bucket

python video_downloader.py -e fpolacov@gmail.com -o $videos_bucket_folder -l '["bucket_"]' -g '["nor_sitting","sitting_peter","sled_sitting","san_sitting","car_sitting","dan_sitting"]' -t '["14_tim"]' --incremental

python prepare_data_for_training.py --all_labels="$all_labels" -l "$all_labels" -i $videos_bucket_folder -t '["14_tim"]' -o $dataset_bucket -m $model_name --remove_movement #--search_frames_on_path=../ARThermal

rm $full_dataset -rf

cp $acted_dataset $full_dataset -r

cp $dataset_bucket/* $full_dataset -r

./nfolds_CNN.sh $model_name 1