import tensorflow as tf
import numpy as np
import os
import time
import datetime
from tensorflow.contrib import learn
from semantic_similituder.input_helpers import InputHelper

"""
reference : https://github.com/dhwajraj/deep-siamese-text-similarity
"""
def comparator(batch_size, eval_path, vocab_path, model_path):
    result_list = []

    inpH = InputHelper()

    x1_test, x2_test, y_test = inpH.getTestDataSet(eval_path, vocab_path, 30)

    graph = tf.Graph()
    with graph.as_default():
        session_conf = tf.ConfigProto(
            allow_soft_placement=True,
            log_device_placement=False)
        sess = tf.Session(config=session_conf)
        with sess.as_default():
            # Load the saved meta graph and restore variables
            saver = tf.train.import_meta_graph("{}.meta".format(model_path))
            sess.run(tf.global_variables_initializer())
            saver.restore(sess, model_path)

            # Get the placeholders from the graph by name
            input_x1 = graph.get_operation_by_name("input_x1").outputs[0]
            input_x2 = graph.get_operation_by_name("input_x2").outputs[0]
            input_y = graph.get_operation_by_name("input_y").outputs[0]

            dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]
            # Tensors we want to evaluate
            predictions = graph.get_operation_by_name("output/distance").outputs[0]

            accuracy = graph.get_operation_by_name("accuracy/accuracy").outputs[0]

            sim = graph.get_operation_by_name("accuracy/temp_sim").outputs[0]

            batches = inpH.batch_iter(list(zip(x1_test, x2_test, y_test)), 2 * batch_size, 1, shuffle=False)

            all_predictions = []
            all_d = []
            for db in batches:
                x1_dev_b, x2_dev_b, y_dev_b = zip(*db)
                batch_predictions, batch_acc, batch_sim = sess.run([predictions, accuracy, sim],
                                                                   {input_x1: x1_dev_b, input_x2: x2_dev_b,
                                                                    input_y: y_dev_b, dropout_keep_prob: 1.0})
                all_predictions = np.concatenate([all_predictions, batch_predictions])
                # print(batch_predictions)
                all_d = np.concatenate([all_d, batch_sim])
                # print("DEV acc {}".format(batch_acc))
            for ex in all_predictions:
                result_list.append(ex)
            correct_predictions = float(np.mean(all_d == y_test))
            print("Accuracy: {:g}".format(correct_predictions))

    return result_list
