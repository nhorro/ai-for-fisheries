# Darknet con GPU para entrenamiento de modelos

Docker con compilación de [fork de AlexeyAB de darknet](https://github.com/AlexeyAB/darknet) para GPU.

```bash
./build.sh
```

Para preparar dataset seguir instrucciones de la wiki del repositorio oficial.

Apuntar TRAINING_PATH a ruta donde se encuentre el dataset.

Por ejemplo, para kaggle-fisheries-yolo:

```bash
export TRAINING_PATH=${PWD}/data/datasets/kaggle-fisheries-yolo
docker run --rm -it -p 8090:8090 -v $TRAINING_PATH:/training --runtime=nvidia --shm-size=4g  darknet-gpu /bin/bash
```

Adentro del docker (modo interactivo):

```bash
./darknet detector train /training/fisheries.data /training/yolo-fisheries.cfg yolov4.conv.137 -dont_show -map
```