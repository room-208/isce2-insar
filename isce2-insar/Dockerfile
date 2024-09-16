FROM isce/isce2:latest

COPY requirements.txt .

RUN apt update && \
    apt install -y git curl python3-pip zip unzip nano

RUN pip install --upgrade pip setuptools && \
    pip install -r requirements.txt