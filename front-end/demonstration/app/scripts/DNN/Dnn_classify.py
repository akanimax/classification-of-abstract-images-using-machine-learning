import pandas
import keras
import numpy as np
import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from keras.models import load_model

class DnnClassifier:
	model = load_model('/home/ccenter/new/17-02-2017_clone/BE/Data/Models/Model1/DnnClassifier.h5')
	label_probability = {}

	def __init__(self):
		pass
	def initializeLabels(self):
		dataframe = pandas.read_csv("final.csv",header=None)
		dataset = dataframe.values
		Y = dataset[:,8]

		# encode class values as integers
		encoder = LabelEncoder()
		encoder.fit(Y)
		encoded_Y = encoder.transform(Y)
		# convert integers to dummy variables (i.e. one hot encoded)
		dummy_y = np_utils.to_categorical(encoded_Y)
		numpy.save('classes.npy', encoder.classes_)

	def returnProbabilities(self,features):
		encoder=LabelEncoder()
		encoder.classes_ = numpy.load('/home/ccenter/new/17-02-2017_clone/BE/Data/Models/Model1/classes.npy')
		print(features)
		probs =self.model.predict_proba(np.array([features]),verbose=1)
		print(probs)
		for i in range (10):
			self.label_probability[encoder.inverse_transform(i)]=probs[0][i]
		print(self.label_probability)
		
	def returnClassPred(self):
		encoder = LabelEncoder()
		encoder.classes_ = numpy.load('/home/ccenter/new/17-02-2017_clone/BE/Data/Models/Model1/classes.npy')
		predictions = self.model.predict_classes(np.array([[1000,23,2,23,43,7,234,2]]))
		print (predictions)
		print (encoder.inverse_transform(predictions))		
		for i in range (10):
			
			print (encoder.inverse_transform(i))
