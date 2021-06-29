GID= eval "id -g"
docker build -t jupyter-datascience \
	--build-arg USERID=$UID \
	--build-arg GROUPID=$GID \
	--build-arg USERNAME=$USER \
	.