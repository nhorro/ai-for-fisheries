echo $CONDA_PREFIX
darknet detector map kaggle-fisheries.data \
                     ../../models/kaggle-fisheries-yolo/kaggle-fisheries-yolo4.cfg \
                     ../../models/kaggle-fisheries-yolo/kaggle-fisheries-yolo4.weights \
                     -iou_thresh 0.5 -points 101 > yolo4-model-performance-report.txt

