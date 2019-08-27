FROM centos:7

ENV PYTHON_VERSION 3.6.4

RUN yum -y groupinstall -y "Development Tools" && \
    yum -y update && \
    yum -y install openssl-devel zlib-devel wget && \
    wget https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tar.xz && \
    tar -xJf Python-$PYTHON_VERSION.tar.xz && \
    cd Python-$PYTHON_VERSION && \
    ./configure && \
    make && \
    make install && \
    pip3 install --upgrade pip && \
    pip3 install tensorflow==2.0.0-rc0
