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
	model = load_model('./keras_model/DnnClassifier.h5')
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

	def returnProbabilities(self):
		probs =self.model.predict_proba(np.array([[1000,23,2,23,43,7,234,2]]),verbose=1)
		print(probs)
	def returnClassPred(self):
		encoder = LabelEncoder()
		encoder.classes_ = numpy.load('classes.npy')
		predictions = self.model.predict_classes(np.array([[1000,23,2,23,43,7,234,2]]))
		print (predictions)
		print (encoder.inverse_transform(predictions))
obj=DnnClassifier()
obj.returnProbabilities()
#obj.initializeLabels()
obj.returnClassPred()
