FROM tensorflow/tensorflow:0.8.0
RUN apt-get update && apt-get install -y language-pack-ja && \
  apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip install flask flask-cors gunicorn awscli
RUN mkdir -p /tmp/image
ENV LANG=ja_JP.UTF-8
COPY ./src /opt/tensor-api

VOLUME /tmp/gunicorn

WORKDIR /opt/tensor-api
CMD gunicorn app:app -c guniconf.py
