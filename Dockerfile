FROM alpine:latest
FROM python:3.5-alpine
MAINTAINER Downey "downeytqualitya@gmail.com"

WORKDIR /usr/src/app

#Add source file
COPY . /usr/src/app
  
RUN python setup.py install \
    &&echo $PWD 
WORKDIR tentrr
RUN echo $PWD
#ENTRYPOINT golem run Tentrr full_regression
CMD golem gui
#CMD["golem","run","Tentrr","full_regression”]
