docker run --rm \
		   --user=$UID \
		   -p 10000:8888 \
		   -e JUPYTER_ENABLE_LAB=yes \
		   -e CHOWN_HOME=yes \
		   -e CHOWN_HOME_OPTS='-R' \
		   -v "${PWD}":/home/jovyan/work \
		   jupyter-datascience:latest
		   jupyter notebook --NotebookApp.token='' --NotebookApp.password=''