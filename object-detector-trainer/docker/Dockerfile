FROM docker.io/nvidia/cuda:10.1-cudnn7-devel-ubuntu18.04

RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

# To save you a headache
#ENV LC_ALL=C.UTF-8
#ENV LANG=C.UTF-8
#ENV LIBRARY_PATH /usr/local/cuda/lib64/stubs

# Install needed libraries
RUN apt-get update && \
	apt-get upgrade -y && \
	apt-get install -y clang-format wget apt-utils build-essential\
	checkinstall cmake pkg-config yasm git vim curl\
	autoconf automake libtool libopencv-dev build-essential

# Install python-dev and pip
RUN apt-get update && apt-get install -y python3-pip python3.6-dev

# Install all needed python librarires 
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

# Fetch Repo
RUN git clone https://github.com/AlexeyAB/darknet.git 
WORKDIR darknet

# Make
RUN \ 
	sed -i 's/OPENCV=0/OPENCV=1/g' Makefile && \
	sed -i 's/GPU=0/GPU=1/g' Makefile && \
	sed -i 's/CUDNN=0/CUDNN=1/g' Makefile && \
	make

RUN wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.conv.137 	