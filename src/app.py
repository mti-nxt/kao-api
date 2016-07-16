#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
from datetime import datetime
import tensorflow as tf
import subprocess
import base64
import os

app = Flask(__name__)
CORS(app)

sess = tf.Session()

@app.route("/healthcheck")
def healthcheck():
  return "OK"

@app.route("/api/face", methods=["POST"])
def classify():
  data = request.data
  tmpPath = "/tmp/image/" + datetime.now().strftime('%s') + ".jpg"
  tmp = open(tmpPath,"w")
  tmp.write(base64.b64decode(data))
  tmp.close()
  # tmpPathを使ってこの後解析用の関数を読んで結果を返す
  result = {
    "host_rate": 0.9,
    "villain_rate": 0.99,
    "jhonnys_rate": 0.1,
    "yoshimoto_rate": 0.05,
  }
  # 解析した後、tmpの画像は削除する
  os.remove(tmpPath)
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
  result = subprocess.check_call("aws s3 cp s3://kao-class-dev/kao-api %s/data --recursive" % os.getcwd(), shell=True)
  return "refreshed"

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8080)
