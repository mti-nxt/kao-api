FROM tensorflow/tensorflow:0.8.0
RUN apt-get update && apt-get install -y language-pack-ja && \
  apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip install flask
ENV LANG=ja_JP.UTF-8
COPY ./src /opt/tensor-api
EXPOSE 8080
WORKDIR /opt/tensor-api
CMD python app.py
