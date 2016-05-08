# TensorFlowに[Connexion](https://github.com/zalando/connexion)ベースのAPIでアクセスするベース

* [Connexion](https://github.com/zalando/connexion)というAPIフレームワークを利用しています
    * [Flask](http://flask.pocoo.org/)をベースにしたフレームワークです
    * Flaskではアノテーションでルーティングしますが、Connexionは[Swagger](http://swagger.io/getting-started/)の定義を元にルテーティングしてくれます。
        * 引数のチェックなどもある程度やってくれます
    * [swagger-codegen](https://github.com/swagger-api/swagger-codegen) で生成されたものに手を加えました
* 基本的には[docker-compose](https://docs.docker.com/compose/)で起動する想定になっています
    * ローカルにTensorflowを`pip install`しても動かせると思います
* とりあえず適当に``tensorflow.Session().run()``だけしてみています

## ディレクトリ構成

```
.
├── Dockerfile            ...tensorflowをpython3で動かすイメージの定義
├── README.md
├── docker-compose.yml    ...とりあえずローカルで動かすためのcompose定義
├── dockerignore
└── src                   ...pythonのソースコードを格納する
    ├── app.py
    ├── controllers       ...各APIの中身を記述する
    └── swagger.yaml      ...APIインターフェース定義
```

## 使い方

### 起動方法

```
$ docker-compose up
```

で起動し、 http://localhost:8080/api/ui/ でSwagger製のAPIドキュメントを参照することができます。

### 止め方

`Ctrl+C`で止まることもあれば止まらないことも・・・（謎）  

```
$ docker-compose down
```

が確実です。


## アーキテクチャメモ

### Dockerベース

最終的にAmazonECSで動作させるつもりなのでDockerイメージで動作するように組んであります。 
See: [Dockerfile](Dockerfile)

### Python3ベース

ConnexionはPython2.7でも動くと書いてあるのですが、実際には動かず。  
Googleから公式に配布されているDockerイメージ[gcr.io/tensorflow/tensorflow](https://www.tensorflow.org/versions/r0.8/get_started/os_setup.html#docker-installation)はPython2.7ベースでConnexionが動かず。

仕方がないので[公式のDockerfile](https://github.com/tensorflow/tensorflow/blob/r0.8/tensorflow/tools/docker/Dockerfile)を[フォークしてPython3ベースのイメージを自前で作成](https://hub.docker.com/r/newgyu/tensorflow/)。  
(Python3.5ではなく、3.4なのはベースイメージでapt-get installで入れられるバージョンが3.4だったからです)

### src以下をコンテナにマウント

`./src` -> `/opt/tensor-api` のマウントを[docker-compose.yml](docker-compose.yml)に定義してあります。