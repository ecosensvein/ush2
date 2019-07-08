FROM python:3.6.4-alpine3.7


COPY ./requirements.txt /code/requirements.txt
WORKDIR /code/

RUN apk --update add build-base mysql-dev bash
RUN pip install --no-cache-dir -r requirements.txt


COPY . /code/

EXPOSE 80
