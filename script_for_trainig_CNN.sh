#!/bin/sh
#

if [ $# -lt 1 ]; then
    echo $0: usage: script_for_training_CNN.sh model_name opt
    exit 1
fi

model_name=$1
tim=4_tim
today=$(date '+%d-%m-%Y')
output_dir=trained_models/"$model_name"_"$today"

mkdir $output_dir

if [ $# -gt 2 ]; then
rm -rf $output_dir/*

#download videos of user validation
#python video_downloader.py -e v@v.com -o ../videos_validation
#download videos of user data_collection
python video_downloader.py -e d@d.com -o ../videos_data_collection
#download videos of user data
python video_downloader.py -e d@d.dd -o ../videos_data

#python prepare_data_for_training.py -i ../videos_validation -o ../dataset -m $model_name
python prepare_data_for_training.py -i ../videos_data_collection -o ../dataset -m $model_name
python prepare_data_for_training.py -i ../videos_data -o ../dataset -m $model_name
fi

if [ $# -gt 1 ]; then
python prepare_data_for_training.py -o ../dataset -m $model_name --only_dataset | tee $output_dir/output_"$model_name".txt
fi

mv ../dataset/$tim/"$model_name"* $output_dir

cd ../../ccv/bin
sudo ./image-net --train-list ../../thermix/ARTraining/$output_dir/"$model_name"_training.txt --test-list ../../thermix/ARTraining/$output_dir/"$model_name"_testing.txt --base-dir ../../thermix/dataset --working-dir ../../thermix/ARTraining/$output_dir/"$model_name".sqlite3 | tee -a ../../thermix/ARTraining/$output_dir/output_"$model_name".file

cd ../../thermix/ARTraining
output_filepath=./$output_dir/output_"$model_name".file runipy plot_ccv_thermix.ipynb
