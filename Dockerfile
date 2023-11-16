FROM python:3.9-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /code

COPY requirements.txt *.py ./

RUN pip install --no-cache-dir -r requirements.txt && \
    useradd -m myuser

USER myuser
