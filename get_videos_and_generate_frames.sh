#!/bin/bash

#only downloaded
#./make_day_demo_video_of_group.sh ../ARThermal/videos_black5 Irene_001 black5@bramblexpress.com 1 1 true true '["14_tim"]' &
#./make_day_demo_video_of_group.sh ../ARThermal/videos_black5 Irene_002 black5@bramblexpress.com 1 1 true true '["14_tim"]' &
#./make_day_demo_video_of_group.sh ../ARThermal/videos_golden5s Rick_001 golden5s@bramblexpress.com 1 1 true true '["14_tim"]' &
#./make_day_demo_video_of_group.sh ../ARThermal/videos_golden5s Luke_001 golden5s@bramblexpress.com 1 1 true true '["14_tim"]' &
#./make_day_demo_video_of_group.sh ../ARThermal/videos_black5 Irene_003 black5@bramblexpress.com 1 1 true true '["14_tim"]' &
#./make_day_demo_video_of_group.sh ../ARThermal/videos_golden5s Charles_003 golden5s@bramblexpress.com 1 1 true true '["14_tim"]' &
#./make_day_demo_video_of_group.sh ../ARThermal/videos_ipod5 Luke_002 ipod@ipod.com 1 1 true true '["14_tim"]' &
#./make_day_demo_video_of_group.sh ../ARThermal/videos_golden5s Charles_004 golden5s@bramblexpress.com 1 1 true true '["14_tim"]' &
#./make_day_demo_video_of_group.sh ../ARThermal/videos_ipod5 Julien_002 ipod@ipod.com 1 1 true true '["14_tim"]' &
#./make_day_demo_video_of_group.sh ../ARThermal/videos_black5 Anne_007 black5@bramblexpress.com 1 1 true true '["14_tim"]' &
#./make_day_demo_video_of_group.sh ../ARThermal/videos_golden5s Charles_005 golden5s@bramblexpress.com 1 1 true true '["14_tim"]' &
#./make_day_demo_video_of_group.sh ../ARThermal/videos_ipod5 Rick_002 ipod@ipod.com 1 1 true true '["14_tim"]' &
#./make_day_demo_video_of_group.sh ../ARThermal/videos_golden5s Anne_008 golden5s@bramblexpress.com 1 1 true true '["14_tim"]' &
#./make_day_demo_video_of_group.sh ../ARThermal/videos_black5 Julien_003 black5@bramblexpress.com 1 1 true true '["14_tim"]' &

#./make_day_demo_video_of_group.sh ../ARThermal/videos_ipod5 Henry_007 ipod@ipod.com 1 1 true true '["14_tim"]' &
#./make_day_demo_video_of_group.sh ../ARThermal/videos_golden5s Anne_009 golden5s@bramblexpress.com 1 1 true true '["14_tim"]' &
#./make_day_demo_video_of_group.sh ../ARThermal/videos_black5 Erika_001 black5@bramblexpress.com 1 1 true true '["14_tim"]' &

#cd thermix/ && source bin/activate && cd ARTraining

##### DOWNLOADING NOW #####

#t1 one per section
#./prepare_for_YOLO.sh Anne_008 ../ARThermal/videos_golden5s golden5s@bramblexpress.com
#./prepare_for_YOLO.sh Rick_002 ../ARThermal/videos_ipod5 ipod@ipod.com
#./prepare_for_YOLO.sh Julien_003 ../ARThermal/videos_black5 black5@bramblexpress.com
#t2 one per section
#./prepare_for_YOLO.sh Anne_009 ../ARThermal/videos_golden5s golden5s@bramblexpress.com
#./prepare_for_YOLO.sh Henry_007 ../ARThermal/videos_ipod5 ipod@ipod.com
#./prepare_for_YOLO.sh Erika_001 ../ARThermal/videos_black5 black5@bramblexpress.com
#t3 one per section
#./prepare_for_YOLO.sh Marge_008 ../ARThermal/videos_golden5s golden5s@bramblexpress.com
./prepare_for_YOLO.sh April_001 ../ARThermal/videos_ipod5 ipod@ipod.com
./prepare_for_YOLO.sh Erika_002 ../ARThermal/videos_black5 black5@bramblexpress.com
#pending
./prepare_for_YOLO.sh Marge_009 ../ARThermal/videos_golden5s golden5s@bramblexpress.com
./prepare_for_YOLO.sh April_002 ../ARThermal/videos_ipod5 ipod@ipod.com
./prepare_for_YOLO.sh Erika_003 ../ARThermal/videos_black5 black5@bramblexpress.com
./prepare_for_YOLO.sh Marge_010 ../ARThermal/videos_golden5s golden5s@bramblexpress.com

#t4 end
./make_day_demo_video_of_group.sh ../ARThermal/videos_ipod5 April_001 ipod@ipod.com 1 1 true true '["14_tim"]' 
./make_day_demo_video_of_group.sh ../ARThermal/videos_golden5s Marge_008 golden5s@bramblexpress.com 1 1 true true '["14_tim"]'
./make_day_demo_video_of_group.sh ../ARThermal/videos_black5 Erika_002 black5@bramblexpress.com 1 1 true true '["14_tim"]'

#t4 one per session
./make_day_demo_video_of_group.sh ../ARThermal/videos_ipod5 April_002 ipod@ipod.com 1 1 true true '["14_tim"]'
./make_day_demo_video_of_group.sh ../ARThermal/videos_golden5s Marge_009 golden5s@bramblexpress.com 1 1 true true '["14_tim"]'
./make_day_demo_video_of_group.sh ../ARThermal/videos_black5 Erika_003 black5@bramblexpress.com 1 1 true true '["14_tim"]'
./make_day_demo_video_of_group.sh ../ARThermal/videos_golden5s Marge_010 golden5s@bramblexpress.com 1 1 true true '["14_tim"]'

##### PENDING #####
./make_day_demo_video_of_group.sh ../ARThermal/videos_golden5s Marge_010 golden5s@bramblexpress.com 1 1 true true '["14_tim"]'

### NOT IN DB YET ###
#./prepare_for_YOLO.sh Erika_004 ../ARThermal/videos_black5 black5@bramblexpress.com
#MARGE011 DESCARTADO
#./prepare_for_YOLO.sh Marge_012 ../ARThermal/videos_golden5s golden5s@bramblexpress.com

#MARGE011 DESCARTADO
#./make_day_demo_video_of_group.sh ../ARThermal/videos_golden5s Marge_012 golden5s@bramblexpress.com 1 1 true true '["14_tim"]'
#./make_day_demo_video_of_group.sh ../ARThermal/videos_black5 Erika_004 black5@bramblexpress.com 1 1 true true '["14_tim"]'

##### NOT READY FOR DOWNLOAD #####
#./make_day_demo_video_of_group.sh ../ARThermal/videos_ipod5 April_003 ipod@ipod.com 1 1 true true '["14_tim"]'

echo "All finished"

#finished
#./make_day_demo_video_of_group.sh ../ARThermal/videos_ipod5 Julien_001 ipod@ipod.com 1 1 true true '["14_tim"]'
#./make_day_demo_video_of_group.sh ../ARThermal/videos_ipod5 Charles_002 ipod@ipod.com 1 1 true true '["14_tim"]'
#./make_day_demo_video_of_group.sh ../ARThermal/videos_ipod5 Charles_001 ipod@ipod.com 1 1 true true '["14_tim"]'
#./make_day_demo_video_of_group.sh ../ARThermal/videos_ipod5 Henry_006 ipod@ipod.com 1 1 true true
#./make_day_demo_video_of_group.sh ../ARThermal/videos_golden5s Anne_006 golden5s@bramblexpress.com 1 1 true true
#./make_day_demo_video_of_group.sh ../ARThermal/videos_black5 Marge_007 black5@bramblexpress.com 1 1 true true
#./make_day_demo_video_of_group.sh ../ARThermal/videos_black5 Marge_006 black5@bramblexpress.com 1 1 true true
#./make_day_demo_video_of_group.sh ../ARThermal/videos_golden5s Anne_005 golden5s@bramblexpress.com 1 1 true true
#./make_day_demo_video_of_group.sh ../ARThermal/videos_ipod5 Victor_006 ipod@ipod.com 1 1 true true
#./make_day_demo_video_of_group.sh ../ARThermal/videos_black5 Marge_003 black5@bramblexpress.com 1 1 true true
#./make_day_demo_video_of_group.sh ../ARThermal/videos_golden5s Anne_001 golden5s@bramblexpress.com 1 1 true true
#./make_day_demo_video_of_group.sh ../ARThermal/videos_ipod5 Victor_004 ipod@ipod.com 1 1 true true
#./make_day_demo_video_of_group.sh ../ARThermal/videos_golden5s Anne_003 golden5s@bramblexpress.com 1 1 true true
#./make_day_demo_video_of_group.sh ../ARThermal/videos_black5 Marge_005 black5@bramblexpress.com 1 1 true true
#./make_day_demo_video_of_group.sh ../ARThermal/videos_ipod5 Victor_005 ipod@ipod.com 1 1 true true
#./make_day_demo_video_of_group.sh ../ARThermal/videos_black5 Marge_004 black5@bramblexpress.com 1 1 true true
#./make_day_demo_video_of_group.sh ../ARThermal/videos_golden5s Anne_002 golden5s@bramblexpress.com 1 1 true true
#./make_day_demo_video_of_group.sh ../ARThermal/videos_golden5s Anne_004 golden5s@bramblexpress.com 1 1 true true
#./make_day_demo_video_of_group.sh ../ARThermal/videos_ipod5 sarmiento_008 ipod@ipod.com 1 1 true true
#./make_day_demo_video_of_group.sh ../ARThermal/videos_golden5s sarmiento_005 golden5s@bramblexpress.com 1 1 true true
#./make_day_demo_video_of_group.sh ../ARThermal/videos_golden5s sarmiento_007 golden5s@bramblexpress.com 1 1 true true