# TensorFlowに[Flask](http://flask.pocoo.org/)ベースのAPIでアクセスするベース

*  [Flask](http://flask.pocoo.org/)というWEBフレームワークを利用しています
    * [swagger.yml](src/swagger.yml)は connexionベースでやろうとしていた時の名残で飾りです。
* 基本的には[docker-compose](https://docs.docker.com/compose/)で起動する想定になっています
* とりあえず適当に``tensorflow.Session().run()``だけしてみています

## ディレクトリ構成

```
├── Dockerfile          ...tensorflow+flaskでAPIを動かすイメージの定義
├── README.md
├── docker-compose.yml    ...とりあえずローカルで動かすためのcompose定義
├── dockerignore
├── nginx               ...リクエストを受けるNginx
│   ├── Dockerfile
│   └── nginx.conf
└── src
    ├── app.py          ...起動ファイル。（今はベタにここに全部書いてあります）
    ├── guniconf.py
    └── swagger.yaml
```

## 使い方

### 起動方法

```
$ docker-compose up
```

で起動し、 http://localhost:8080/healthcheck でとりあえず起動確認。  
(Win/Macはdocker-machineのIP  192.168.99.100)

### 止め方

`Ctrl+C`で止まった風に見えますが、

```
$ docker-compose down
```

で、止めてください。（docker-composeのバージョンによるのかも)

## アーキテクチャメモ

### Dockerベース

See: 

* [Dockerfile](Dockerfile)
* [Dockerfile](nginx/Dockerfile)

### Python2ベース

Googleから公式に配布されているDockerイメージ[gcr.io/tensorflow/tensorflow](https://www.tensorflow.org/versions/r0.8/get_started/os_setup.html#docker-installation)はPython2.7ベースなのでそれに乗っかる。


### src以下をコンテナにマウント

`./src` -> `/opt/tensor-api` のマウントを[docker-compose.yml](docker-compose.yml)に定義してあります。
ローカルで動かすときにいちいち`docker-compose build`するの面倒かなーと思って。

## apiテストするときのコマンド
base64 -i input.jpg -o ./sampledata
curl -X POST -H "Content-Type: text/plain" -d @sampledata 'localhost:8080/api/face
