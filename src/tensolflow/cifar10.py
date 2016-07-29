#!/usr/bin/env python
#! -*- coding: utf-8 -*-

import sys
import numpy as np
import tensorflow as tf

#この辺の設定はkao-learnerに合わせること　ずれると死にます
NUM_CLASSES = 4
IMAGE_SIZE = 28
IMAGE_PIXELS = IMAGE_SIZE*IMAGE_SIZE*3

def inference(images_placeholder, keep_prob):
    """ モデルを作成する関数

    引数: 
      images_placeholder: inputs()で作成した画像のplaceholder
      keep_prob: dropout率のplace_holder

    返り値:
      cross_entropy: モデルの計算結果
    """
    def weight_variable(shape):
      initial = tf.truncated_normal(shape, stddev=0.1)
      return tf.Variable(initial)

    def bias_variable(shape):
      initial = tf.constant(0.1, shape=shape)
      return tf.Variable(initial)

    def conv2d(x, W):
      return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

    def max_pool_2x2(x):
      return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                            strides=[1, 2, 2, 1], padding='SAME')
    
    x_image = tf.reshape(images_placeholder, [-1, 28, 28, 3])

    with tf.name_scope('conv1') as scope:
        W_conv1 = weight_variable([5, 5, 3, 32])
        b_conv1 = bias_variable([32])
        h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)

    with tf.name_scope('pool1') as scope:
        h_pool1 = max_pool_2x2(h_conv1)
    
    with tf.name_scope('conv2') as scope:
        W_conv2 = weight_variable([5, 5, 32, 64])
        b_conv2 = bias_variable([64])
        h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)

    with tf.name_scope('pool2') as scope:
        h_pool2 = max_pool_2x2(h_conv2)

    with tf.name_scope('fc1') as scope:
        W_fc1 = weight_variable([7*7*64, 1024])
        b_fc1 = bias_variable([1024])
        h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
        h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)
        h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

    with tf.name_scope('fc2') as scope:
        W_fc2 = weight_variable([1024, NUM_CLASSES])
        b_fc2 = bias_variable([NUM_CLASSES])

    with tf.name_scope('softmax') as scope:
        y_conv=tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

    return y_conv

#変数の設定
images_placeholder = tf.placeholder("float", shape=(None, IMAGE_PIXELS))
labels_placeholder = tf.placeholder("float", shape=(None, NUM_CLASSES))
keep_prob = tf.placeholder("float")

logits = inference(images_placeholder, keep_prob)

sess = tf.InteractiveSession()
#Saverを使ってチェックポイントファイルをロード
saver = tf.train.Saver()
sess.run(tf.initialize_all_variables())
saver.restore(sess, "./data/model.ckpt")

#　こいつをapiで呼びだす！
def calc_similarity(image_filename, ckpt_filename):
    # データを読み込んで28x28に縮小
    jpeg_r = tf.read_file(image_filename)
    decode_image = tf.image.decode_jpeg(jpeg_r, channels=3)
    resize_image = tf.image.resize_images(decode_image, IMAGE_SIZE, IMAGE_SIZE)
    # 一列にした後、0-1のfloat値にする
    reshape_image = tf.reshape(resize_image, [-1])
    test_image = tf.Session().run(reshape_image).astype(np.float32) / 255.0
    
    #各クラスの推定値の配列　桁がだいぶ違うのでスケール調整が必要な感じ　とりあえずこのままでも結果は出力される
    pred = logits.eval(feed_dict={images_placeholder: [test_image], keep_prob: 1.0})[0]
    return pred

#このファイル単体でもテスト確認できるようにmainの場合はtest.jpgの判定を行ない、4出力の値を表示する
if __name__ == '__main__':
    print(calc_similarity("./test.jpg","model.ckpt"))
