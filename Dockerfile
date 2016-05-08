FROM newgyu/tensorflow:0.8.0-py34
RUN pip3 install connexion
#COPY ./src /opt/tensor-api
EXPOSE 8080
WORKDIR /opt/tensor-api
ENV LANG=ja_JP.UTF-8
CMD python3 app.py
