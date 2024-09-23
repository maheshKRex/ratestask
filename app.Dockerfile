FROM python:3.12

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements-test.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
RUN pip install python-dotenv

COPY . /usr/src/app/