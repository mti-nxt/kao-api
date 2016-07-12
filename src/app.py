#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import jsonify
from flask_cors import CORS
import tensorflow as tf
import subprocess
import os

app = Flask(__name__)
CORS(app)

sess = tf.Session()
#TODO ここでチェックポイントファイルをセッションにロードするやつを書く

@app.route("/healthcheck")
def healthcheck():
  return "OK"

@app.route("/api/face", methods=["POST"])
def classify():
    #TODO ここでチェックポイントファイルを使って判定する処理を書く
  result = {
    "host_rate": 0.9,
    "villain_rate": 0.99,
    "jhonnys_rate": 0.1,
    "yoshimoto_rate": 0.05
  }
  return jsonify(result)

@app.route("/api/face/<int:sampleId>", methods=["GET"])
def classify_sample(sampleId):
  a = tf.constant(10)
  b = tf.constant(32)
  r = sess.run(a + b)
  result = {
    "host_rate": 0.4,
    "villain_rate": 0.32,
    "jhonnys_rate": 0.1,
    "yoshimoto_rate": r.item(0)  #numpyは直でJSON Serializeできない・・・
  }
  return jsonify(result)

@app.route("/api/chkpoint", methods=["PUT"])
def reload_chkpoint():
    #TODO ここでもチェックポイントファイルをリロードする
  result = subprocess.check_call("aws s3 cp s3://kao-class-dev/kao-api %s/data --recursive" % os.getcwd(), shell=True)
  return "refreshed"

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8080)
