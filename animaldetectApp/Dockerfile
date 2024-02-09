FROM python:3.9

WORKDIR /usr/src/animaldetectpod

RUN apt-get -y update

RUN apt-get install -y ffmpeg libsm6 libxext6

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY  . /usr/src/animaldetectpod

CMD [ "python", "main.py" ]