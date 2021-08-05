echo $CONDA_PREFIX
MODEL_NAME=kaggle-fisheries
darknet detector map \
                 $MODEL_NAME.data \
                 $MODEL_NAME-yolo4.cfg \
                 backup/${MODEL_NAME}-yolo4_best.weights \
                 -iou_thresh 0.5 -points 101 \
                 > ${MODEL_NAME}-perf-report.txt

