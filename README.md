# TensorFlowに[Flask](http://flask.pocoo.org/)ベースのAPIでアクセスするベース

*  [Flask](http://flask.pocoo.org/)というWEBフレームワークを利用しています
    * swagger.ymlは connexionベースでやろうとしていた時の名残で飾りです。
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
    └── app.py            ...起動ファイル。（今はベタにここに全部書いてあります）
```

## 使い方

### 起動方法

```
$ docker-compose up
```

で起動し、 http://localhost:8080/api/ui/ でSwagger製のAPIドキュメントを参照することができます。

### 止め方

`Ctrl+C`で止まった風に見えますが、

```
$ docker-compose down
```

で、止めてください。


## アーキテクチャメモ

### Dockerベース

デプロイが楽なのでAmazonECSでやりたかったのですが、なぜかECSからTensorFlow入のイメージを起動するとクッソ遅いという問題に突き当たり、諦めました。
でもやっぱ周辺ライブラリのインストールがめんどくさいので非ECSなDockerベースでやるつもり。

See: [Dockerfile](Dockerfile)

### Python2ベース

Googleから公式に配布されているDockerイメージ[gcr.io/tensorflow/tensorflow](https://www.tensorflow.org/versions/r0.8/get_started/os_setup.html#docker-installation)はPython2.7ベースなのでそれに乗っかる。


### src以下をコンテナにマウント

`./src` -> `/opt/tensor-api` のマウントを[docker-compose.yml](docker-compose.yml)に定義してあります。
ローカルで動かすときにいちいち`docker-compose build`するの面倒かなーと思って。