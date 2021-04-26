FROM ubuntu:20.04

ARG user_id
ARG group_id
ARG user_name

USER root

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y \
	libopencv-dev \
        python3-pip \
	python3-opencv && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install tensorflow && \
    pip3 install numpy pandas sklearn matplotlib seaborn jupyter pyyaml h5py && \
    pip3 install keras --no-deps && \
    pip3 install opencv-python && \
    pip3 install imutils

# Jupyter and Tensorboard ports
EXPOSE 8888 6006

# User no root
RUN apt-get update --allow-releaseinfo-change -y  && \
    apt-get clean -y  && \
	apt-get install --fix-missing -y sudo && \
    useradd -m $user_name && echo "$user_name:$user_name" | chpasswd    && \
    adduser $user_name sudo    && \
    echo "\n$user_name ALL=(ALL:ALL) NOPASSWD: ALL" >> /etc/sudoers  && \
    chown -R $user_name:$user_name /home/$user_name

COPY conf/.jupyter /home/$user_name/.jupyter
COPY run_jupyter.sh /home/$user_name/

WORKDIR /home/$user_name
USER $user_name

CMD ["/home/$user_name/run_jupyter.sh"]