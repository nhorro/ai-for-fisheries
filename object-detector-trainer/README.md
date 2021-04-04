# Darknet con GPU para entrenamiento de modelos

Docker con compilación de [fork de AlexeyAB de darknet](https://github.com/AlexeyAB/darknet) para GPU.

```bash
cd docker
./build.sh
```

Para preparar dataset seguir instrucciones de la wiki del repositorio oficial.

```bash
export TRAINING_PATH=~/workspace/ai-for-fisheries/data/datasets/kaggle-fisheries-yolo
docker run --rm -it -p 8090:8090 -v $TRAINING_PATH:/training --runtime=nvidia --shm-size=1g  darknet-gpu /bin/bash
```

Adentro del docker:

```bash
./darknet detector train /training/fisheries.data /training/yolo-fisheries.cfg yolov4.conv.137 -dont_show
```

