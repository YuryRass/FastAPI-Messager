FROM python:3.11-alpine

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR .

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY ./external__main  /external__main
COPY ./internal__messager /internal__messager
COPY ./internal__worker /internal__worker
