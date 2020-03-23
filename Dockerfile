FROM centos:7

ENV SOURCE_DIRECTORY /tmp/project
ENV PYTHON_VERSION 3.7.4

RUN yum -y groupinstall -y "Development Tools" && \
    yum -y update && \
    yum -y install sqlite-devel openssl-devel zlib-devel libffi libffi-devel wget && \
    wget https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tar.xz && \
    tar -xJf Python-$PYTHON_VERSION.tar.xz && \
    cd Python-$PYTHON_VERSION && \
    ./configure --enable-loadable-sqlite-extensions && \
    make && \
    make install && \
    pip3 install --upgrade pip && \
    pip3 install tensorflow==2.1.0 tensorflow_probability==0.8.0 numpy
