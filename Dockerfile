From python:3-alpine
ENV PYTHONUNBUFFERED 1# Creating working directory
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY . /code/

RUN apk add --no-cache bash

RUN apk add --update docker openrc
RUN rc-update add docker boot
RUN docker run --help
RUN apk add py3-setuptools
RUN pip install -r requirements.txt


EXPOSE 8000
RUN ls
CMD ["python", "manage.py", "runserver" , "0.0.0.0:8000"]

