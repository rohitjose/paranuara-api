FROM python:3.7-alpine
LABEL maintainer="rohitjose@gmail.com"

RUN apk add --no-cache build-base libffi-dev libressl-dev linux-headers

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user