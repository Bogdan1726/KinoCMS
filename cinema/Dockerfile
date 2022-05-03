FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

RUN pip install --upgrade pip
COPY  ./requirements.txt /usr/src/app
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y gettext

COPY . /usr/src/app




