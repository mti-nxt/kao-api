from flask import jsonify
import tensorflow as tf

# 顔認識APIのコントローラー
# URLとメソッドとのひも付けはswagger.yamlの
#  x-swagger-router-controller
#  operationId
# で定義する

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

def classify(data) -> str:
  result = {
    "host_rate": 0.9,
    "villain_rate": 0.99,
    "jhonnys_rate": 0.1,
    "yoshimoto_rate": 0.05
  }
  return jsonify(result)
