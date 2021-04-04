# Darknet con GPU para entrenamiento de modelos

Docker con compilación de [fork de AlexeyAB de darknet](https://github.com/AlexeyAB/darknet) para GPU.

```bash
cd docker
./build.sh
```

Para preparar dataset seguir instrucciones de la wiki del repositorio oficial.

```bash
export TRAINING_PATH= # ...
docker run --rm -it -v TRAINING_PATH:/training --runtime=nvidia darknet-gpu /bin/bash
```

