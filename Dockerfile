#      _      _                     ___        __                              
#     | | ___| |_ ___  ___  _ __   |_ _|_ __  / _| ___ _ __ ___ _ __   ___ ___ 
#  _  | |/ _ \ __/ __|/ _ \| '_ \   | || '_ \| |_ / _ \ '__/ _ \ '_ \ / __/ _ \
# | |_| |  __/ |_\__ \ (_) | | | |  | || | | |  _|  __/ | |  __/ | | | (_|  __/
#  \___/ \___|\__|___/\___/|_| |_| |___|_| |_|_|  \___|_|  \___|_| |_|\___\___|
#
# https://github.com/yqlbu/jetson-inference-native
#
# Author: Copyright (c) 2020, NVIDIA CORPORATION. All rights reserved.
#
# Modifier: Copyright (C) 2020-2021 Kevin Yu <https://hikariai.net>
#
# This is a open-source software, liscensed under the MIT License.
# See /License for more information.

FROM nvcr.io/nvidia/l4t-pytorch:r32.5.0-pth1.7-py3

# set maintainer
LABEL maintainer "Kevin Yu"

ENV TZ=Asia/Shanghai \
    SHELL=/bin/bash

WORKDIR jetson-inference-native

# install pre-requisite packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    cmake \
    curl \
    python3-opencv \
    && rm -rf /var/lib/apt/lists/*

# set TZ
RUN echo $TZ > /etc/timezone && apt-get install -y tzdata && \
    dpkg-reconfigure tzdata && locale-gen en_US.UTF-8 

# pip dependencies for pytorch-ssd
RUN pip3 install --verbose --upgrade Cython && \
    pip3 install --verbose boto3 pandas

# alias python3 -> python
RUN rm /usr/bin/python && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    ln -s /usr/bin/pip3 /usr/bin/pip

# copy source
COPY c c
COPY calibration calibration
COPY examples examples
COPY plugins plugins
COPY python python
COPY tools tools
COPY utils utils
COPY CMakeLists.txt CMakeLists.txt
COPY CMakePreBuild.sh CMakePreBuild.sh
COPY src src
COPY data data

# build jetson-inference from source
RUN mkdir docs && \
    touch docs/CMakeLists.txt && \
    sed -i 's/nvcaffe_parser/nvparsers/g' CMakeLists.txt && \
    mkdir build && \
    cd build && \
    cmake ../ && \
    make -j$(nproc) && \
    make install && \
    /bin/bash -O extglob -c "cd /jetson-inference-native/build; rm -rf -v !(aarch64|download-models.*)" && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /jetson-inference-native/src

# install api-server dependencies
RUN pip3 install -r requirements.txt

# expose port
EXPOSE 5000

# define entrypoint
CMD ["python", "server.py"]

