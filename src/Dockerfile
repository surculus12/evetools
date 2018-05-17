FROM python:3-alpine3.7

COPY ./src/requirements.txt /requirements.txt
RUN pip install --upgrade pip \
 && pip install -r requirements.txt \
 && rm -f /requirements.txt

WORKDIR /app
COPY ./src /app
