FROM jupyter/tensorflow-notebook
MAINTAINER Nicolás Eduardo Horro <nhorro@gmail.com>

#ENV OPENCV_VERSION 3.0.0

USER root
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y \
	libopencv-dev \
    python3-pip \
	python3-opencv && \
    rm -rf /var/lib/apt/lists/*

# Install in the default python3 environment
RUN pip install --quiet --no-cache-dir opencv-python imutils imgaug && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"    

# Jupyter and Tensorboard ports
EXPOSE 8888 6006

# Back to the default directory
WORKDIR /home/$NB_USER/work

# Switch back to notebook user
USER $NB_USER