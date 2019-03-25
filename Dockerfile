FROM python:3.6-alpine

ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
