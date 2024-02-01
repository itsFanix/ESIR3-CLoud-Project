# syntax=docker/dockerfile:1

FROM python:3.9

WORKDIR /downscale-app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY  . /downscale-app

EXPOSE 5000

ENTRYPOINT  [ "flask", "run", "--host=0.0.0.0" ]