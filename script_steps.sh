#!/bin/sh
#

if [ $# -lt 1 ]; then
    echo $0: usage: script_for_training_CNN.sh model_name opt
    exit 1
fi

model_name=$1
tim=14_tim
#today=$(date '+%d-%m-%Y')
#today=12-06-2016
output_dir=trained_models/"$model_name"

dataset_dir=../dataset_merged
#dataset_dir=../dataset_poses_people_background
#dataset_dir=../dataset_thermalRaw_no_movement_2
#dataset_dir=../dataset_thermal_pose

all_labels='["lying","sitting","standing","people","background"]'
all_labels_classes='["1","2","3","4","5"]'
prepare_data_for_training="prepare_data_for_training.py -l $all_labels --all_labels=$all_labels"
#prepare_data_for_training=prepare_data_for_training.py
#prepare_data_for_training=prepare_data_for_training_pose.py

mkdir -p $output_dir

if [ $# -gt 1 ]; then
python $prepare_data_for_training -o $dataset_dir -m $model_name -t '["'"$tim"'"]' --only_dataset | tee $output_dir/output_"$model_name".txt

mv $dataset_dir/$tim/"$model_name"* $output_dir

#generate dataset videos
mov_dir=../mov_dataset_"$model_name"
if [ ! -d $mov_dir ]; then
python video_from_images.py -c $all_labels_classes -i $dataset_dir  -t $tim -o $mov_dir -f '["'"$output_dir"/"$model_name"'_files.txt"]' --text=THERMIX

cd youtube_upload
for filepath in $(ls -f ../$mov_dir/*); do
        video_name=$(basename "$filepath")
        python upload_video.py --file=../$mov_dir/$video_name \
        --title=dataset_"$video_name" --privacyStatus="private"
done
cd ..
fi

else 
mv $dataset_dir/$tim/"$model_name"* $output_dir
fi

cd ../../ccv/bin
#sudo ./image-net --train-list ../../thermix/ARTraining/$output_dir/"$model_name"_training.txt --test-list ../../thermix/ARTraining/$output_dir/"$model_name"_testing.txt --base-dir ../../thermix/ARTraining/$dataset_dir --working-dir ../../thermix/ARTraining/$output_dir/"$model_name".sqlite3 | tee -a ../../thermix/ARTraining/$output_dir/output_"$model_name".file
echo demo | sudo -S ./step1 --train-list ../../thermix/ARTraining/$output_dir/"$model_name"_training.txt --test-list ../../thermix/ARTraining/$output_dir/"$model_name"_testing.txt --base-dir ../../thermix/ARTraining/$dataset_dir --working-dir ../../thermix/ARTraining/$output_dir/"$model_name".sqlite3 | tee -a ../../thermix/ARTraining/$output_dir/output_"$model_name".file

cd ../../thermix/ARTraining
output_filepath=./$output_dir/output_"$model_name".file runipy plot_ccv_thermix.ipynb
cd ../../ccv/bin

echo demo | sudo -S ./step2 --train-list ../../thermix/ARTraining/$output_dir/"$model_name"_training.txt --test-list ../../thermix/ARTraining/$output_dir/"$model_name"_testing.txt --base-dir ../../thermix/ARTraining/$dataset_dir --working-dir ../../thermix/ARTraining/$output_dir/"$model_name".sqlite3 | tee -a ../../thermix/ARTraining/$output_dir/output_"$model_name".file

cd ../../thermix/ARTraining
output_filepath=./$output_dir/output_"$model_name".file runipy plot_ccv_thermix.ipynb
cd ../../ccv/bin

echo demo | sudo -S ./step3 --train-list ../../thermix/ARTraining/$output_dir/"$model_name"_training.txt --test-list ../../thermix/ARTraining/$output_dir/"$model_name"_testing.txt --base-dir ../../thermix/ARTraining/$dataset_dir --working-dir ../../thermix/ARTraining/$output_dir/"$model_name".sqlite3 | tee -a ../../thermix/ARTraining/$output_dir/output_"$model_name".file

cd ../../thermix/ARTraining
output_filepath=./$output_dir/output_"$model_name".file runipy plot_ccv_thermix.ipynb
