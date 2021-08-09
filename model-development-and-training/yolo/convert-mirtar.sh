MODEL_NAME=mirtar
INPUT_SIZE=416

cd tensorflow-yolov4-tflite

MODELS_BASE_PATH=../../../data/models/
MODEL_PATH=$MODELS_BASE_PATH/${MODEL_NAME}-yolo/

# Copy obj names
echo "Copying obj.names from original model to ./data/classes"
cp $MODEL_PATH/obj.names data/classes/obj.names

# Convert to tensorflow
echo "Converting model to tensorflow..."
python3 save_model.py --weights $MODEL_PATH/$MODEL_NAME-yolo4.weights \
                      --output  $MODEL_PATH/checkpoints/yolo-${INPUT_SIZE} \
                      --input_size $INPUT_SIZE --model yolov4

cd ..
