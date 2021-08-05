MODELS_BASE_PATH=../../models/
MODEL_NAME=mirtar

# YOLO4
cp backup/$MODEL_NAME-yolo4_best.weights $MODELS_BASE_PATH/$MODEL_NAME-yolo/$MODEL_NAME-yolo4.weights
cp $MODEL_NAME-yolo4.cfg $MODELS_BASE_PATH/$MODEL_NAME-yolo/
cp obj.names $MODELS_BASE_PATH/$MODEL_NAME-yolo/
cp kaggle-fisheries-perf-report.txt $MODELS_BASE_PATH/$MODEL_NAME-yolo/
