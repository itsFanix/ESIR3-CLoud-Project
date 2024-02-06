FROM python:3.9

WORKDIR /usr/src/animaldetectpod

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY  . /usr/src/animaldetectpod

CMD [ "python", "AnimalDectect.py" ]