#!/bin/bash

data_path=/workspace/data/thermix_data/frames_no_movement
yolo_path=/workspace/third_party/YOLO_tensorflow
exec_path=$(pwd)

cd $exec_path

groups_for_yolo=""
for filepath in $(ls -t $data_path/); do
    filename=$(basename "$filepath")
    if [ -d $data_path/$filepath/15_tim ]; then
    
        filename=$(echo $filename | cut -d'_' -f 1,2)
        groups_for_yolo+=$filename' '
        
    fi
done

groups_for_yolo=${groups_for_yolo:0:-1}

echo $groups_for_yolo

cd $yolo_path
for group in $groups_for_yolo; do
    if (( $(cat yolo_log.txt | grep $group | wc -l) > 0 )); then
        echo $group" finished"
        continue
    fi

    echo "processing "$group
    
    python YOLO_small_tf.py -artraining $group
    echo "Finish $group" | tee -a yolo_log.txt
done

cd $exec_path