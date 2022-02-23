# syntax=docker/dockerfile:1
FROM python:3.9-alphine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /AppServer
COPY requirements.txt /AppServer/
RUN pip install -r requirements.txt
COPY . /AppServer/