docker run --rm \
		   --user=$UID \
                   -e NB_UMASK=0x777 \
		   -p 10000:8888 \
		   -e JUPYTER_ENABLE_LAB=yes \
		   -e CHOWN_HOME=yes \
		   -e CHOWN_HOME_OPTS='-R' \
		   -v "${PWD}":/home/jovyan/work \
		   nhorro/jupyter-datascience:latest
		   ./start-singleuser.sh
