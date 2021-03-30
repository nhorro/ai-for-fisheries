# Detector de objetos con YOLOv4

Ambiente de ejecución para detector de objetos con YOLOv4 usando DNN de OpenCV (master).

Contenido:

~~~
dockers
    |-cpu Docker basado en Ubuntu 18.04 c/ compilación de OpenCV sin CUDA.
    |-gpu Docker basado en NVIDIA Ubuntu 18.04/CUDA c/ compilación de OpenCV
app
~~~

- ./dockers Dockers con compilación de branch master de OpenCV para CPU y GPU.

## Instrucciones de uso

Modo interactivo.

Iniciar docker (CPU).

~~~bash
docker run --rm -it -v $PWD:/work --workdir /work ubuntu18-opencv4 /bin/bash
~~~

Procesar una imagen.

~~~bash
python3 detect.py --input data/fisheries1.jpeg --model-weights="./coco/yolov4.weights" --model-cfg="./coco/yolov4.cfg" --classes-txt="./coco/classes.txt"
~~~

~~~bash
python3 detect.py --input data/fisheries1.jpeg --model-weights="./fisheries/yolov4.weights" --model-cfg="./fisheries/yolov4.cfg" --classes-txt="./fisheries/classes.txt"
~~~

Procesar un video.

~~~bash
python3 detect.py --input data/fisheries1.jpeg --model-weights="./fisheries/yolov4.weights" --model-cfg="./fisheries/yolov4.cfg" --classes-txt="./fisheries/classes.txt"
~~~

Procesar un lote de datos.

~~~bash
python3 detect.py --input data/fisheries1.jpeg --model-weights="./fisheries/yolov4.weights" --model-cfg="./fisheries/yolov4.cfg" --classes-txt="./fisheries/classes.txt"
~~~

Como servicio.

WIP:
    - Ver permisos capture device.
    - Integración con DeepSORT?
    - Escritura de salida
    - Logging