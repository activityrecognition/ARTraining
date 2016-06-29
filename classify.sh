#!/bin/bash

#model's name
model_name=thermix_30a

dataset_base_dir=/media/Gui2/thermix/suenos_dorados_day
tim=14_tim
label_id=3

tim_print=4_tim

#directory where the original validation images are located
data_dir=$dataset_base_dir/$tim/$label_id

#directory of the model to run in order to classify the images
model_dir=/media/Gui2/thermix/ARTraining/trained_models/"$model_name"
#path to .sqlite of the model
model_sqlite_path="$model_dir"/"$model_name".sqlite3
#path to .words of the model
model_words_path="$model_dir"/"$model_name"._words
#directory of output files of the model's classification
out_dir="$model_dir"/classification_output/$tim_print/$label_id

rm -rf $out_dir
mkdir -p $out_dir

#lib ccv's bin directory where cnnclassify.c is located
ccv_dir=/media/Gui2/ccv/bin

# switch to ccv's directory to run classifier
cd $ccv_dir

for folder in $(ls -d $data_dir/*); do
    folder_name=$(basename "$folder")
    print_folder_name=$dataset_base_dir/$tim_print/$label_id/"${folder_name:0:-2}"
    mkdir -p $out_dir/${folder_name:0:-2}
    for filepath in $(ls -f $folder/*); do
        filename=$(basename "$filepath" | cut -d. -f1)
        output_filepath=$out_dir/${folder_name:0:-2}/"$filename".png
        aux_1=$( echo $filename | cut -d_ -f 1 );aux_2=$( echo $filename | cut -d_ -f 2 );print_filename=$(echo $[$aux_1 * 3 + $aux_2])
        echo "$filepath => $output_filepath"
        ./cnnclassify "$filepath" "$model_sqlite_path" | ./cnndraw.rb "$model_words_path" $print_folder_name/"$print_filename".png $output_filepath
    done
done

# go to output directory
cd $out_dir
