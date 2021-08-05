echo $CONDA_PREFIX
MODEL_NAME=kaggle-fisheries
./darknet detector map $MODEL_NAME.data $MODEL_NAME-yolo4tiny.cfg backup/$MODEL_NAME_best.weights -iou_thresh 0.5 -points 101 > $MODEL_NAME-perf-report.txt