FROM isce/isce2:latest

COPY requirements.txt .

RUN apt update && \
    apt install -y git curl python3-pip zip unzip nano

RUN pip install --upgrade pip setuptools && \
    pip install -r requirements.txt

ENV ISCE_HOME=/usr/lib/python3.8/dist-packages/isce/
ENV PATH=$ISCE_HOME/applications:$PATH