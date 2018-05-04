# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os
import time

import numpy as np
import tensorflow as tf


def load_graph(model_file):
  graph = tf.Graph()
  graph_def = tf.GraphDef()

  with open(model_file, "rb") as f:
    graph_def.ParseFromString(f.read())
  with graph.as_default():
    tf.import_graph_def(graph_def)

  return graph


def read_tensor_from_image_file(file_name,
                                input_height=299,
                                input_width=299,
                                input_mean=0,
                                input_std=255):
  input_name = "file_reader"
  output_name = "normalized"
  file_reader = tf.read_file(file_name, input_name)
  if file_name.endswith(".png"):
    image_reader = tf.image.decode_png(
        file_reader, channels=3, name="png_reader")
  elif file_name.endswith(".gif"):
    image_reader = tf.squeeze(
        tf.image.decode_gif(file_reader, name="gif_reader"))
  elif file_name.endswith(".bmp"):
    image_reader = tf.image.decode_bmp(file_reader, name="bmp_reader")
  else:
    image_reader = tf.image.decode_jpeg(
        file_reader, channels=3, name="jpeg_reader")
  float_caster = tf.cast(image_reader, tf.float32)
  dims_expander = tf.expand_dims(float_caster, 0)
  resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
  normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
  sess = tf.Session()
  result = sess.run(normalized)

  return result


def load_labels(label_file):
  label = []
  proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
  for l in proto_as_ascii_lines:
    label.append(l.rstrip())
  return label

def parse_file_path(root_path, suffix):
    target_file_list = []
    target_class_list = []
    if os.path.exists(root_path):
        for sub_dir in os.listdir(root_path):
            sub_dir_path = os.path.join(root_path, sub_dir)
            for target_file in os.listdir(sub_dir_path):
                if target_file.endswith(suffix):
                    target_file_list.append(os.path.join(sub_dir_path, target_file))
                    target_class_list.append(sub_dir)
    return target_file_list, target_class_list

def evaluate_image(image_path, graph):
    t = read_tensor_from_image_file(
        image_path,
        input_height=input_height,
        input_width=input_width,
        input_mean=input_mean,
        input_std=input_std)

    input_name = "import/" + input_layer
    output_name = "import/" + output_layer
    input_operation = graph.get_operation_by_name(input_name)
    output_operation = graph.get_operation_by_name(output_name)

    with tf.Session(graph=graph) as sess:
      results = sess.run(output_operation.outputs[0], {
          input_operation.outputs[0]: t
      })
    results = np.squeeze(results)

    top_k = results.argsort()[-5:][::-1]
    labels = load_labels(label_file)
    # for i in top_k:
    #   print(labels[i], results[i])
    return labels, results, top_k

def output_static_result(total_ratio, class_count_list, correct_count_list, test_path_out):
    with open(test_path_out, 'w') as f:
        f.write(str(total_ratio) + '\n')
        for idx in range(len(class_count_list)):
            if class_count_list[idx] > 0:
                f.write(str(float(correct_count_list[idx] / class_count_list[idx])) + '\n')
            else:
                f.write('0\n')
    return

if __name__ == "__main__":
    file_name = "tensorflow/examples/label_image/data/grace_hopper.jpg"
    model_file = \
        "tensorflow/examples/label_image/data/inception_v3_2016_08_28_frozen.pb"
    label_file = "tensorflow/examples/label_image/data/imagenet_slim_labels.txt"
    input_height = 299
    input_width = 299
    input_mean = 0
    input_std = 255
    input_layer = "input"
    output_layer = "InceptionV3/Predictions/Reshape_1"
    test_out_path = "test_results.txt"
    file_dir = ""
    suffix = ".jpg"

    parser = argparse.ArgumentParser()
    parser.add_argument("--image", help="image to be processed")
    parser.add_argument("--graph", help="graph/model to be executed")
    parser.add_argument("--labels", help="name of file containing labels")
    parser.add_argument("--input_height", type=int, help="input height")
    parser.add_argument("--input_width", type=int, help="input width")
    parser.add_argument("--input_mean", type=int, help="input mean")
    parser.add_argument("--input_std", type=int, help="input std")
    parser.add_argument("--input_layer", help="name of input layer")
    parser.add_argument("--output_layer", help="name of output layer")
    parser.add_argument("--test_out_path", help="test results path")
    parser.add_argument("--file_dir", help="images directory")
    parser.add_argument("--suffix", help="valid images suffix with '.'")
    args = parser.parse_args()

    if args.graph:
        model_file = args.graph
    if args.image:
        file_name = args.image
    if args.labels:
        label_file = args.labels
    if args.input_height:
        input_height = args.input_height
    if args.input_width:
        input_width = args.input_width
    if args.input_mean:
        input_mean = args.input_mean
    if args.input_std:
        input_std = args.input_std
    if args.input_layer:
        input_layer = args.input_layer
    if args.output_layer:
        output_layer = args.output_layer
    if args.test_out_path:
        test_out_path = args.test_out_path
    if args.file_dir:
        file_dir = args.file_dir
    if args.suffix:
        suffix = args.suffix

    # target_file_list, target_class_list = parse_file_path("/Users/zchholmes/src_images/movedImages", ".jpg")
    target_file_list, target_class_list = parse_file_path(file_dir, suffix)

    class_num = len(os.listdir(file_dir))
    total_count = len(target_file_list)
    print(class_num)
    print(total_count)

    class_count_list = [0 for i in range(class_num)]
    correct_count_list = [0 for i in range(class_num)]
    correct_count = 0

    graph = load_graph(model_file)

    start_time = time.time()
    # for idx in range(100):
    for idx in range(len(target_file_list)):
        class_count_list[int(target_class_list[idx])] += 1
        print('@{}'.format(idx))
        labels, results, top_k = evaluate_image(target_file_list[idx], graph)
        top_1 = top_k[0]
        if target_class_list[idx] == labels[top_1]:
            correct_count += 1
            correct_count_list[int(target_class_list[idx])] += 1
        print('{} <> {} ~~ {}'.format(target_class_list[idx], labels[top_1], results[top_1]))
        print('============> {} sec'.format(time.time() -start_time))
        # for i in top_k:
        #     print(labels[i], results[i])
    print(class_count_list)
    print(correct_count_list)

    output_static_result(float(correct_count/total_count), class_count_list, correct_count_list, test_out_path)