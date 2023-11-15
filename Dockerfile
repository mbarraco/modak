FROM python:3.9-slim-buster
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY *.py ./

RUN useradd -m myuser
USER myuser

