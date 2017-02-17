from __future__ import print_function
import tensorflow as tf
from Helpers.CNN_Creator import *
import os
from PIL import Image
import PIL
import numpy as np
from scipy import ndimage
import cPickle as pickle

def get_predictions(path):
	graph = tf.Graph()

	''' Neural network name: BotNet
		Size: medium
		conf: conv => conv => pool => conv => pool => fc => fc => softmax'''


	'''Set the constant paths here'''
	# set the paths required for the script to work:
	root = "/home/ccenter/new/17-02-2017_clone/BE/Data/"
	pickle_file_path = root + "Data_pindown.pickle"
	log_path = root + "logs"


	# define the constants required hence forth:
	batch_size = 500
	patch_size = 5
	num_hidden = 256

	image_size = 100
	num_labels = 10
	num_channels = 3 # rgb images
	image_depth = 3

	with graph.as_default():

		# Input data.
		with tf.name_scope("INPUTS"):
		    tf_image_single = tf.placeholder(tf.float32, shape=(1, image_size, image_size, num_channels), name="Data")

		    # tf_valid_dataset = tf.constant(cv_dataSet, name="cross_validation_dataset")
		    # tf_test_dataset = tf.constant(test_dataSet, name="test_dataset")

		# Model.
		def model(data):
		    # CONV LAYER
		    # layer has 8 (3 x 3) convoluting filters
		    layer1_1 = addConvLayer(data, [patch_size, patch_size, num_channels, 8],
		                            "lay_1.1_w", "lay_1.1_b", tf.nn.sigmoid)


		    # CONV LAYER
		    # layer has 12 (3 x 3) convoluting filters
		    layer2_1 = addConvLayer(layer1_1, [patch_size, patch_size, 8, 12],
		                            "lay_2.1_w", "lay_2.1_b", tf.nn.sigmoid)


		    # CONV LAYER
		    # layer has 16 (3 x 3) convoluting filters
		    layer3_1 = addConvLayer(layer2_1, [patch_size, patch_size, 12, 16],
		                            "lay_3.1_w", "lay_3.1_b", tf.nn.sigmoid)


		    # POOL LAYER
		    # will not require any data variable or parameter holder
		    # a simple 2 x 2 max_pooling operation
		    layer4_1 = addPoolLayer(layer3_1, [1, 2, 2, 1], [1, 2, 2, 1])

		    # CONV LAYER
		    # layer has 20 (3 x 3) convoluting filters
		    layer5_1 = addConvLayer(layer4_1, [patch_size, patch_size, 16, 20],
		                            "lay_5.1_w", "lay_5.1_b", tf.nn.sigmoid)

		    # FC LAYER
		    # input dimension will be: 8 * 8 * 32
		    # length, width calculation: 32 =first pool=> 16 =second pool=> 8
		    # depth calculation: 32 ...(same as the last conv output)
		    # output dimension: 128 ...(equal to number of hidden cells)
		    # number of hidden cells: 128
		    # reshape the tensor before passing it to the FC layers
		    shape = layer5_1.get_shape().as_list()
		    reshape = tf.reshape(layer5_1, [shape[0], shape[1] * shape[2] * shape[3]])
		    layer6_1 = addFCLayer(reshape, [shape[1] * shape[2] * shape[3], num_hidden],
		                          "lay_6.1_w", "lay_6.1_b", tf.nn.sigmoid)

		    # FC LAYER
		    # input dimension will be: 256
		    # output dimension will be: 256
		    # number of hidden cells: 256
		    layer7_1 = addFCLayer(layer6_1, [num_hidden, num_hidden],
		                          "lay_7.1_w", "lay_7.1_b", tf.nn.sigmoid)

		    # Fianl output layer for the neural network
		    layer8_1 = addFCLayer(layer7_1, [num_hidden, num_labels],
		                          "lay_8.1_w", "lay_8.1_b", tf.nn.sigmoid)

		    return layer8_1

		# Training computation.
		logits = model(tf_image_single)

		# with tf.name_scope("Loss"):
		#     loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits, tf_train_labels))
		#     tf.summary.scalar("loss", loss)

		# Optimizer.
		# with tf.name_scope("train_step"):
		#     optimizer = tf.train.GradientDescentOptimizer(0.1).minimize(loss)

		# Predictions for the training, validation, and test data.
		with tf.name_scope("train_prediction"):
		    class_prediction = tf.nn.softmax(logits)

		# with tf.name_scope("validation_prediction"):
		    # validation_prediction = tf.nn.softmax(model(tf_valid_dataset))




	with tf.Session(graph=graph) as session:
		saver = tf.train.Saver()

		# code to restore the session:
		saver.restore(session, os.path.join(root, "Models/Model1/mod_1.ckpt"))

		# get the label mappings
		label_mappings = {}
		with open(os.path.join(root, "label_mappings.pickle"), "rb") as f:
			label_mappings = pickle.load(f)
		
		label_mappings = dict([(label_mappings[k], k) for k in label_mappings.keys()])

		img = Image.open("/home/ccenter/new/17-02-2017_clone/BE/front-end/demonstration/media/" + path)
		img = img.resize((image_size, image_size), PIL.Image.ANTIALIAS)

		img = np.array(img).astype(float)

		print(img.shape)
		if(img.shape != (image_size, image_size, image_depth)):
			print("padding the image")
			padded_image = np.zeros((image_size, image_size, image_depth), dtype=float)
			padded_image[:, :, 0] = img
			img = padded_image

		# reshape the img to get the required shape
		image = np.ndarray(shape=(1, image_size, image_size, image_depth), dtype=np.float32)
		image[0, :, :, :] = img


		# check what the value of "name_of_some_bringer" is:
		predictions = session.run(class_prediction, feed_dict={tf_image_single: image})
	

		tups = zip([x for x in range(len(label_mappings))], list(predictions[0]))


		labelled_predictions = []
		for (index, value) in tups:
			labelled_predictions.append((label_mappings[index], value))		
	
		return sorted(labelled_predictions, key= lambda x: x[1], reverse=True)
