FROM alpine:latest
FROM python:3.7-alpine
MAINTAINER Downey "downeytqualitya@gmail.com"

WORKDIR /usr/src/app

#Add source file
COPY . /usr/src/app
  
RUN python setup.py install \
    &&echo $PWD 
WORKDIR H5G
RUN echo $PWD
CMD golem gui

