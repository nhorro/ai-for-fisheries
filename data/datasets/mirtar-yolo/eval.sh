echo $CONDA_PREFIX
darknet detector map mirtar.data \
                     ../../models/mirtar-yolo/mirtar-yolo4.cfg \
                     ../../models/mirtar-yolo/mirtar-yolo4.weights \
                     -iou_thresh 0.5 -points 101 > yolo4-model-performance-report.txt

