#!/bin/bash

./prepare_for_YOLO.sh Julien_001 ../ARThermal/videos_ipod5 ipod@ipod.com &
./prepare_for_YOLO.sh Luke_002 ../ARThermal/videos_ipod5 ipod@ipod.com &

wait

./prepare_for_YOLO.sh Irene_003 ../ARThermal/videos_black5 black5@bramblexpress.com &
./prepare_for_YOLO.sh Julien_002 ../ARThermal/videos_ipod5 ipod@ipod.com &

wait

./prepare_for_YOLO.sh Charles_005 ../ARThermal/videos_golden5s golden5s@bramblexpress.com &
./prepare_for_YOLO.sh Anne_007 ../ARThermal/videos_black5 black5@bramblexpress.com &