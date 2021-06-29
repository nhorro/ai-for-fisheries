# jupyter-datascience (modificado)

- Variante de docker oficial de [jupyter datascience-notebook](https://hub.docker.com/r/jupyter/datascience-notebook) con librerías adicionales para procesamiento de imagen y video: opencv, imaug, etc.
- Uso principal: preparación de datos, ensayos de algoritmos y generación de reportes. Para inferencia se recomienda usar otro entorno con soporte para GPU.

Uso:

~~~bash
cd $WORKSPACE_PATH
docker run --rm \
		   --user=$UID \
		   -p 10000:8888 \
		   -e JUPYTER_ENABLE_LAB=yes \
		   -e CHOWN_HOME=yes \
		   -e CHOWN_HOME_OPTS='-R' \
		   -v "${PWD}":/home/jovyan/work \
		   jupyter-datascience:latest
		   jupyter notebook --NotebookApp.token='' --NotebookApp.password=''
~~~