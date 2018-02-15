# Use an official Python runtime as a parent image
FROM python:2.7-slim

RUN mkdir -p /spider
WORKDIR /spider/
RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN ln -s /spider/start-crawl /usr/sbin/start-crawl
RUN ln -s /spider/shub-image-info /usr/sbin/shub-image-info
ADD . /spider/