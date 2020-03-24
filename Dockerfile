FROM python:3.7.4-slim

RUN apt update && \
    apt install -y curl iputils-ping net-tools vim

RUN pip install flask && \
    mkdir /app

COPY app.py /app

CMD ["python", "/app/app.py"]
