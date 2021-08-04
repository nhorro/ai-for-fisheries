echo $CONDA_PREFIX
MODEL_NAME=kaggle-fisheries
darknet detector train $MODEL_NAME.data $MODEL_NAME-yolo4tiny.cfg yolov4-tiny.conv.29 -json_port 8070 -mjpeg_port 8090 -ext_output -dont_show -map > ./logs/darknet_logs.log 2>&1 &