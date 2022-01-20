FROM python:3.8-slim

RUN apt update

RUN apt upgrade

RUN apt install -y vim

RUN apt install -y curl

COPY server.py .

COPY requirements.txt  .

RUN pip install -r requirements.txt 

CMD FLASK_APP=server flask run --host 0.0.0.0