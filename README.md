# IA para pesca

Este repositorio contiene los archivos de un prototipo de utilización de IA para análisis de actividades en videos de CCTV a bordo de buques pesqueros. Se integran componentes que se mantienen en repositorios separados, para formar una cadena completa de procesamiento que se despliega como microservicios con docker-compose.

![diagrama_bloques](assets/diagrama_bloques.png)

Se describe la organización de directorios para el desarrollo y ensayo de componentes y tareas intermedias: ensayos, preparación de datos etc. El objetivo de concentrar todo en un mismo repositorio es poder replicar un ambiente de trabajo en distintas PCs reduciendo al mínimo posible los pasos de configuración. El flujo de trabajo propuesto es para prototipado.

## Contenido

[TOC]

## Introducción

Cada directorio representa una etapa, tarea que requiere scripts, reporte o componente del proyecto. En todos los casos se especifica la entrada esperada y la salida generada. La entrada de una etapa o componente puede ser la salida de un componente o etapa anterior.

## Organización del proyecto

Se reconocen las siguientes actividades y se organiza el proyecto asignando un dirctorio a cada una:

- **Obtención de datos**:
  - **Datos crudos** :  imágenes, videos, etc. sin organizar.
  - **Datasets**: datos organizados para un problema de aprendizaje supervisado. Además, pueden estar organizados para el entrenamiento de un modelo con una herramienta específica (por ejemplo, siguiendo la organización de directorios propuesta por Keras, Darknet, Tensorflow Object Detection API, etc.).
  - **Archivos intermedios**: archivos generados durante algún proceso necesarios para algún procedimiento.
  - **Modelos exportados**: arquitecturas de modelos y/o sus pesos serializados luego del entrenamiento para uso posterior en inferencia. Pueden tener distintos formatos, por ejemplo Tensorflow, TensorRT, Scikit Learn, etc.

- **Procedimientos de preparación de datos**: son procedimientos que toman como entrada datos o datasets preparados para un problema de aprendizaje y generan un nuevo dataset. El nuevo dataset puede aportar etiqueado, reorganizar un dataset o aplicarle algún preprocesamiento, como por ejemplo aumentado.

- **Procedimientos de desarrollo y entrenamiento de modelos**: son procedimientos para definir la arquitectura de redes u otros tipos de clasificadores, algoritmos y entrenarlos.
  - **Desarrollo y entrenamiento de modelos**: definición de arquitectura y lazo de entrenamiento.
  - **Conversión y optimización de modelos**: en caso de que aplique, procedimientos para convertir un modelo a otro lenguaje o librería, y eventualmente optimizarlo para algún HW específico.

- **Aplicaciones**: programas que utilizan de la librería [videoanalytics](https://github.com/nhorro/videoanalytics) y los modelos desarrollados para el análisis de videos de pesca. Pueden estar como cuadernos (jupyter), desplegados en forma de servicios con docker-compose, o ambos.

Para los componentes complejos o de propósito general se mantiene un repositorio en github separado.

Este documento describe como clonar estos repositorios en un mismo espacio de trabajo y organizar los archivos de datos y configuración.

Se prone la siguiente organización de directorios. 

```
$WORKSPACE_PATH
    .
    ├── applications
    ├── assets
    ├── data
    │   ├── datasets
    │   │   ├── kaggle-fisheries
    │   │   │   ├── kaggle-ncfm
    │   │   │   ├── test_stg1
    │   │   │   └── train
    │   │   │       ├── ALB
    │   │   │       ├── BET
    │   │   │       ├── DOL
    │   │   │       ├── LAG
    │   │   │       ├── NoF
    │   │   │       ├── OTHER
    │   │   │       ├── SHARK
    │   │   │       └── YFT
    │   │   ├── kaggle-fisheries-yolo
    │   │   │   ├── backup
    │   │   │   ├── data
    │   │   │   └── logs
    │   │   ├── mirtar
    │   │   │   ├── test
    │   │   │   └── train
    │   │   ├── mirtar-aug
    │   │   │   ├── test
    │   │   │   └── train
    │   │   └── mirtar-yolo
    │   │       ├── backup
    │   │       ├── data
    │   │       └── logs
    │   ├── media
    │   │   └── videos-youtube
    │   │       └── cut
    │   ├── models
    │   │   ├── coco
    │   │   ├── kaggle_fisheries
    │   │   ├── kaggle-fisheries-yolo
    │   │   └── yolov4-416-tf
    │   └── other
    ├── data-preparation
    │   ├── kaggle-fisheries
    │   └── mirtar
    ├── doc
    │   └── assets
    ├── dockers
    │   ├── darknet-gpu
    │   └── jupyter-datascience
    ├── model-development-and-training
    │   ├── activity-classifier
    │   ├── feature_extraction
        └── yolo
	README.md
```

Convenciones:

- La ruta absoluta del directorio de espacio de trabajo será referida como $WORKSPACE_PATH.
- Cada componente obtendrá sus entradas y generará sus salidas en el subdirectorio **data**. Nota: con excepción de archivos de configuración u otros de tamaño reducido, el contenido de de este directorio no se mantiene en .git. 
- Por ejemplo:
  - Para preparación de datos se leen los datos originales de **data** y se crea un nuevo directorio con los datos transformados.
  - Para inferencia se leen de **data** los archivos de imagen o video a procesar, pesos del modelo y configuraciones, y se generan en un nuevo directorio las salidas.
- Se adopta la convención para desarrollo con docker de montar el directorio **data** para lectura y escritura. 

## Guía rápida

Actualizado 03/08/2021.
Para trabajar en ambientes sin sudo, se reemplazan los dockers por un ambiente conda para todas las tareas de preparación de datos, desarrollo y entrenamiento de modelos. Se mantiene la convención de uso de data

~~~bash
conda env create -f ai-fisheries.yml
~~~

### Clonar repositorio

```bash
export WORKSPACE_PATH=~/workspace/ai-for-fisheries
mkdir $WORKSPACE_PATH
git clone --recursive https://github.com/nhorro/ai-for-fisheries.git $WORKSPACE_PATH
cd $WORKSPACE_PATH
```

### Importar ambiente conda

```bash
cd $WORKSPACE_PATH
conda env create --file ai-fisheries.yml
```

### Establecer variables de ambiente

```bash
cd $WORKSPACE_PATH
source env.sh 
```

Nota: todos los scripts asument que el directorio raíz es WORKSPACE_PATH.

### Iniciar Jupyter

**Local (opción preferida)**:

```bash
conda activate ai-fisheries
cd $WORKSPACE_PATH
jupyter notebook --NotebookApp.ip='0.0.0.0' --NotebookApp.token='' --NotebookApp.password=''
```

ó

```bash
conda activate ai-fisheries
./run-jupyter-local.sh
```

Docker (pendiente resolver problemas de permisos):

```bash
cd $WORKSPACE_PATH
docker run --rm \
           --user=$UID \
           -p 10000:8888 \
           -e JUPYTER_ENABLE_LAB=yes \
           -e CHOWN_HOME=yes \
           -e CHOWN_HOME_OPTS='-R' \
           -v "${PWD}":/home/jovyan/work \
           nhorro/jupyter-datascience:latest
           jupyter notebook --NotebookApp.token='' --NotebookApp.password=''
```

ó

```bash
./run-jupyter-data-science.sh
```

Nota: este docker contiene Tensorboard en el puerto 6006. Considerar usar otro puerto si se usa en conjunto con dockers para entrenamiento.

### Exportar ambiente conda

```bash
conda env export --name ai-fisheries > ai-fisheries.yml
```

## Instalación y uso de videoanalytics

Las aplicaciones utilizan la librería [videoanalytics](https://github.com/nhorro/videoanalytics), y en algunos casos agregan componentes a la misma.

## Aplicaciones