#!/bin/bash

videos_location="../ARThermal/videos_ipod5" \
group_name="Victor_006" \
tensorbox_input_filepath="../ARThermal/tensorbox_dataset/tensorbox_input.json" \
tensorbox_dataset_dir="../ARThermal/tensorbox_dataset" \
pedestrian_log_filepath="../ARThermal/Victor_006_frames_no_movement/15_tim/sorted_frames_YOLO_results.txt" \
detector_type="yolo" \
runipy add_group_to_tensorbox_input.ipynb