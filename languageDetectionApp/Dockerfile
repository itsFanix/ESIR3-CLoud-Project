
FROM python:3.9

WORKDIR /usr/src/languagepod

RUN apt-get -y update

RUN apt-get install -y ffmpeg

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY  . /usr/src/languagepod

EXPOSE 35000

CMD [ "python", "main.py" ]