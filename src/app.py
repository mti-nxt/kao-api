#!/usr/bin/env python3

from flask import Flask
from flask import jsonify
import tensorflow as tf

app = Flask(__name__)

@app.route("/healthcheck")
def healthcheck() -> str:
  return "OK"

@app.route("/api/face", methods=["POST"])
def classify() -> str:
  result = {
    "host_rate": 0.9,
    "villain_rate": 0.99,
    "jhonnys_rate": 0.1,
    "yoshimoto_rate": 0.05
  }
  return jsonify(result)

@app.route("/api/face/<int:sampleId>", methods=["GET"])
def classify_sample(sampleId) -> str:
  a = tf.constant(10)
  b = tf.constant(32)
  with tf.Session() as sess:
    r = sess.run(a + b)
    result = {
      "host_rate": 0.4,
      "villain_rate": 0.32,
      "jhonnys_rate": 0.1,
      "yoshimoto_rate": r.item(0)  #numpyは直でJSON Serializeできない・・・
    }
    return jsonify(result)

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8080)
 
