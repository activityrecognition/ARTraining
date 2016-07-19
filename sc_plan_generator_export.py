# Copyright 2016 Google Inc. All Rights Reserved.
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

#!/usr/bin/env python2.7
"""Export inception model given existing training checkpoints.
"""

import os.path
import sys

# This is a placeholder for a Google-internal import.

import tensorflow as tf

from tensorflow.models.rnn.translate import seq2seq_model, data_utils
from tensorflow.python.platform import gfile

from tensorflow_serving.session_bundle import exporter

tf.app.flags.DEFINE_integer("epochs",5,"the number of epochs we want this to run")
tf.app.flags.DEFINE_integer("group",5,"the group of the DD_FXS during test")
tf.app.flags.DEFINE_integer("bucket_size",60, "Corresponds to the input bucket size.")
tf.app.flags.DEFINE_float("learning_rate", 0.5, "Learning rate.")
tf.app.flags.DEFINE_float("learning_rate_decay_factor", 0.99,
                          "Learning rate decays by this much.")
tf.app.flags.DEFINE_float("max_gradient_norm", 5.0,
                          "Clip gradients to this norm.")
tf.app.flags.DEFINE_integer("batch_size", 128,
                            "Batch size to use during training.")
tf.app.flags.DEFINE_integer("size", 1024, "Size of each model layer.")
tf.app.flags.DEFINE_integer("num_layers", 3, "Number of layers in the model.")
tf.app.flags.DEFINE_integer("en_vocab_size", 20000, "English vocabulary size.")
tf.app.flags.DEFINE_integer("fr_vocab_size", 20000, "French vocabulary size.")
tf.app.flags.DEFINE_integer("max_train_data_size", 0,
                            "Limit on the size of training data (0: no limit).")
tf.app.flags.DEFINE_integer("steps_per_checkpoint",10,
                            "How many training steps to do per checkpoint.")
tf.app.flags.DEFINE_boolean("decode", False,
                            "Set to True for interactive decoding.")
tf.app.flags.DEFINE_boolean("self_test", False,
                            "Run a self-test if this is set to True.")

tf.app.flags.DEFINE_string('checkpoint_dir', '/tmp/inception_train',
                           """Directory where to read training checkpoints.""")
tf.app.flags.DEFINE_string('export_dir', '/tmp/inception_export',
                           """Directory where to export inference model.""")

FLAGS = tf.app.flags.FLAGS

WORKING_DIR = os.path.dirname(os.path.realpath(__file__))

def file_len(fname):
    with open(fname) as f:
        count =f.read().split('\n')
        totalLineInFile=len(count)
        return totalLineInFile

def export():
    model_folder_base="/Users/colo/Developers/projects/ARSC/_model_May_30_RNN+A/model"
    model_folder = model_folder_base + "1"

    #get the number of lines of a file
    vocab_fr=file_len(model_folder+'/giga-fren.release2.fr')
    print(model_folder)

    FLAGS.checkpoint_dir = str(model_folder)
    FLAGS.export_dir = os.path.join(model_folder,"for_serving")
    FLAGS.size = 512
    FLAGS.num_layers = 2
    FLAGS.bucket_size = 240
    FLAGS.steps_per_checkpoint = 200
    FLAGS.batch_size = 120
    FLAGS.en_vocab_size = 4000
    FLAGS.fr_vocab_size = vocab_fr
    FLAGS.epochs = 5000

    #input_assessment = tf.placeholder(tf.string, shape=(1))

    with tf.Session() as sess:
        """Create translation model and initialize or load parameters in session."""
        buckets = [(FLAGS.bucket_size+1,3)]
        model = seq2seq_model.Seq2SeqModel(
                FLAGS.en_vocab_size, FLAGS.fr_vocab_size, buckets,
                FLAGS.size, FLAGS.num_layers, FLAGS.max_gradient_norm, FLAGS.batch_size,
                FLAGS.learning_rate, FLAGS.learning_rate_decay_factor,
                forward_only=True)
        ckpt = tf.train.get_checkpoint_state(FLAGS.checkpoint_dir)
        if ckpt and gfile.Exists(ckpt.model_checkpoint_path):
            print("Reading model parameters from %s" % ckpt.model_checkpoint_path)
            model.saver.restore(sess, ckpt.model_checkpoint_path)

        # We decode one sentence at a time.
        model.batch_size = 1

        # Load vocabularies.
        en_vocab_path = os.path.join(FLAGS.checkpoint_dir,
                                     "vocab%d.en" % FLAGS.en_vocab_size)
        fr_vocab_path = os.path.join(FLAGS.checkpoint_dir,
                                     "vocab%d.fr" % FLAGS.fr_vocab_size)
        en_vocab, _ = data_utils.initialize_vocabulary(en_vocab_path)
        _, rev_fr_vocab = data_utils.initialize_vocabulary(fr_vocab_path)

        init_op = tf.group(tf.initialize_all_tables(), name='init_op')
        model_exporter = exporter.Exporter(model.saver)
        #signature = exporter.classification_signature(
        #    input_tensor=jpegs, classes_tensor=classes, scores_tensor=values)
        #model_exporter.init(default_graph_signature=signature, init_op=init_op)
        model_exporter.init(sess.graph.as_graph_def(),
                            asset_collection=tf.get_collection(tf.GraphKeys.ASSET_FILEPATHS))
        model_exporter.export(FLAGS.export_dir, tf.constant(model.global_step), sess)
        print('Successfully exported model to %s' % FLAGS.export_dir)



def main(unused_argv=None):
  export()


if __name__ == '__main__':
  tf.app.run()