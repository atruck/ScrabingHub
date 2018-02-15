# Use an official Python runtime as a parent image
FROM python:2.7

RUN wget -q https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2 && \
    tar -xjf phantomjs-2.1.1-linux-x86_64.tar.bz2 && \
    mv phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/bin && \
    rm -rf phantomjs-2.1.1-linux-x86_64.tar.bz2 phantomjs-2.1.1-linux-x86_64

RUN mkdir -p /spider
WORKDIR /spider/
ADD . /spider/
RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN ln -s /spider/start-crawl /usr/sbin/start-crawl
RUN ln -s /spider/shub-image-info /usr/sbin/shub-image-info