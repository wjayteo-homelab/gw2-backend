# syntax=docker/dockerfile:1
FROM python:3.8.12-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
ENV TZ Asia/Singapore
CMD ["python3", "-u", "app.py"]