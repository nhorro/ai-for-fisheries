# Solución para video analítico

Prototipo para explorar formas de extracción de información de video.

Organización del proyecto:

~~~
videonalytics                       Bloques de procesamiento.
videoanalytics-gpu.yml              Ambiente conda (GPU).
README.md                           
~~~

Referencias:
- El código de YOLOv4 y parte de DeepSORT fue adaptado de [yolov4-deepsort](https://github.com/theAIGuysCode/yolov4-deepsort).

## Instrucciones

Importar ambiente conda:

~~~bash
conda env create -f videoanalytics-gpu.yml.
~~~

La forma más sencilla para pruebas y desarrollo es con los notebooks en jupyter.

~~~bash
conda activate videoanalytics-gpu.yml
jupyter notebook .
~~~


## Referencia de componentes

- Fuentes
    - VideoReader
- Sumideros    
    - Detección de objetos
        - YOLOv4Detector
        - DetectorCSV
    - Visualización
        - Anotación de bounding boxes
        - Visualización con Matplotlib
    - Salidas
        - CSV
            - Escritura de detecciones en CSV.
        - DBs
            - Escritura en InfluxDB.
            - Escritura en ElasticSearch.
        - Video
            - Escritura de archivo de video.

## Notas de desarrollo

Exportación de ambiente conda:

~~~bash
conda env export --name yolov4-gpu > videoanalytics-gpu.yml
~~~