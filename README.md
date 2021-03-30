# IA para pesca

Este proyecto consiste en la utilización de IA para monitoreo de actividades a bordo de buques pesqueros. Se integran componentes que se mantienen en repositorios separados, para formar una cadena completa de procesamiento.

Este documento describe la organización de directorios para el desarrollo y ensayo de componentes utilizados.

## Contenido

[TOC]

## Introducción

- Este proyecto consiste en una cadena de procesamiento que integra distintos componentes.

- Todos los componentes esperan una entrada y generan una salida. La entrada puede ser la salida de un componente anterior.

## Organización del proyecto

Componentes:

| Componente              | Entrada                                            | Salida                                                       | Descripción                                      |
| ----------------------- | -------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------ |
| data-preparation        | directorio con dataset                             | directorio o .tar.gz con dataset organizado según lo requerido por el detector y por el object-tracker. | Scripts de preparación de datos.                 |
| object-detector-trainer | dataset preprocesado                               | Pesos de YOLOv4 en formato Darknet. Opcional: conversión a otros formatos. | Entrenador del modelo de detección.              |
| object-detector         |                                                    |                                                              | Componente para realizar detecciones con YOLOv4. |
| object-tracker          | ???                                                |                                                              |                                                  |
| object-tracker-trainer  | ???                                                |                                                              |                                                  |
| processing-pipelines    | - Imágenes/videos a procesar.<br/>- Configuración. | Reporte de detecciones.                                      |                                                  |

Para cada componente se mantiene un repositorio en github separado.

Este documento describe como clonar estos repositorios en un mismo espacio de trabajo y organizar los archivos de datos y configuración.

Se prone la siguiente organización de directorios. 

```
$WORKSPACE_PATH
	|-data-preparation
	|-object-detector-trainer
	|-object-tracker
	|-object-tracker-trainer
	|-tests
	|-processing-pipelines
	|-data
	|-tmp
	README.md
```

Convenciones:

- La ruta absoluta del directorio de espacio de trabajo será referida como $WORKSPACE_PATH.
- Cada componente obtendrá sus entradas y generará sus salidas en $WORKSPACE/data. Nota: con excepción de archivos de configuración u otros de tamaño reducido, el contenido de de este directorio no se mantiene en .git. 

Instrucciones

```bash
export WORKSPACE_PATH=~/workspace/invap-fiuba-proyecto-final
mkdir $WORKSPACE_PATH
cd $WORKSPACE_PATH
```

## Descripción de componentes

### data-preparation

### object-detector-trainer

##### Descripción

Ambiente para entrenamiento de YOLOv4 basado en docker de [BMW Innovation Lab](https://github.com/BMW-InnovationLab/BMW-YOLOv4-Training-Automation).

##### Entradas

- Dataset y archivos de configuración para YOLOv4 preprocesados (ver data-preparation).
- Pesos iniciales de YOLOv4 (se usan los oficiales por defecto)

##### Salidas

- Pesos de modelo entrenado.

##### Setup inicial

```bash
cd object-detector-trainer
git clone --depth=1 https://github.com/BMW-InnovationLab/BMW-YOLOv4-Training-Automation.git
cd BMW-YOLOv4-Training-Automation
sudo docker build -f docker/Dockerfile -t darknet_yolov4_gpu:1 --build-arg GPU=1 --build-arg CUDNN=1 --build-arg CUDNN_HALF=0 --build-arg OPENCV=1 --build-arg DOWNLOAD_ALL=1 .
```

##### Observaciones

### object-detector

Ver: 

Ambiente para inferencia con YOLOv4 basado en docker de [BMW Innovation Lab](https://github.com/BMW-InnovationLab/BMW-YOLOv4-Inference-API-GPU).

### object-tracker

TODO.

### object-tracker-trainer

TODO.

### tests

### processing-pipelines



## Notas de desarrollo