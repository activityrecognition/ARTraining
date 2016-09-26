#PEOPLE DETECTOR Vars

#thermix's group where videos are storaged
#thermix_group=sarmiento_003
thermix_group=$1

#tim='["'14_tim'"]'
#tim=$8
thermal_tim=14_tim

#ccv model name
model_name=thermix_42a

####################
#DO NOT MODIFY BELOW THIS LINE

#folder where raw frames without movement will be saved
frames_dir=/media/Gui2/thermix/ARThermal/frames_no_movement/"$thermix_group"_frames_no_movement

#folder where the ccv model is located
model_folder=/media/Gui2/thermix/ARTraining/trained_models/$model_name

#ccv model name
model_path=$model_folder/$model_name.sqlite3

#filepath that contains the cnn classification
model_results_file=$model_folder/"$thermix_group"_annotations.txt

all_labels='["person","background","'"$thermix_group"'"]'

python prepare_data_for_training.py --all_labels="$all_labels" -l '["'"$thermix_group"'"]' -t '["'"$thermal_tim"'"]' -o $frames_dir -m thermix_1 --only_dataset --only_first_frame_in_dataset

gpu_is_busy=$(nvidia-smi | grep ./cnnclassify | wc -l)
while [ $gpu_is_busy = 2 ]
do
sleep 5s
gpu_is_busy=$(nvidia-smi | grep ./cnnclassify | wc -l)
done

if [ -f $model_results_file ]; then
    results_filepath=$model_results_file \
    dataset_filepath=$frames_dir/$thermal_tim/thermix_1_files.txt \
    output_filepath=$frames_dir/$thermal_tim/thermix_1_files.txt.temp \
    runipy get_non_classified_files.ipynb

    cd ../../ccv/bin
    ./cnnclassify_for_public_dataset $frames_dir/$thermal_tim/thermix_1_files.txt.temp $model_path $frames_dir | tee -a $model_results_file
    
    rm -rf $frames_dir/$thermal_tim/thermix_1_files.txt.temp
else
    cd ../../ccv/bin
    ./cnnclassify_for_public_dataset $frames_dir/$thermal_tim/thermix_1_files.txt $model_path $frames_dir | tee $model_results_file
fi

cd ../../thermix/ARTraining