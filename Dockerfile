FROM python:3.10-slim-bullseye

EXPOSE 18000

LABEL MAINTAINER="James Cotter"
LABEL NAME=solis

RUN mkdir /solis
COPY *.py *.txt /solis

WORKDIR /solis

RUN pip3 install --no-cache-dir -r requirements.txt

CMD [ "python", "./main.py" ]