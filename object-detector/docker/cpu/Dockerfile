FROM ubuntu:18.04

WORKDIR /tmp

# Install minimal prerequisites (Ubuntu 18.04 as reference)
RUN apt update && apt install -y \
					   cmake \
					   g++ \
					   wget \
					   unzip \
					   python3-dev \
					   python3-numpy \
					   libavcodec-dev \
					   libavformat-dev \
					   libswscale-dev \
					   libgstreamer-plugins-base1.0-dev \
					   libgstreamer1.0-dev \
					   libpng-dev \
					   libjpeg-dev \
					   libopenexr-dev \
					   libtiff-dev \
					   libwebp-dev

# Download and unpack sources
RUN wget -O opencv.zip https://github.com/opencv/opencv/archive/master.zip
RUN wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/master.zip
RUN unzip opencv.zip
RUN unzip opencv_contrib.zip

# Create build directory and switch into it
# See: https://docs.opencv.org/master/db/d05/tutorial_config_reference.html
RUN mkdir -p build && cd build \
		  && cmake -DOPENCV_EXTRA_MODULES_PATH=../opencv_contrib-master/modules ../opencv-master \
		   		   -DCMAKE_BUILD_TYPE=RELEASE \ 
		           -DBUILD_opencv_python3=ON \
		           -DOPENCV_ENABLE_NONFREE=ON \
		           -DBUILD_TESTS=OFF \
  				   -DBUILD_PERF_TESTS=OFF \
  				   -DBUILD_EXAMPLES=OFF \
  				   -DBUILD_opencv_apps=OFF \
	 	  && make -j8 \
	 	  && make install \
	 	  && ldconfig