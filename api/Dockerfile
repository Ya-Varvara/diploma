# pull official base image
FROM python:3.11-slim-bookworm

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

# copy requirements file
ADD requirements.txt /app
# install dependencies
RUN pip install -r requirements.txt

# copy project
COPY . /scr/app