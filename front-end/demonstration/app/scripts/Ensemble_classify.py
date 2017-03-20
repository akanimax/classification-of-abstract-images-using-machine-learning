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
from keras.backend.tensorflow_backend import clear_session
import csv
import collections


class EnsembleClassifier:
	
	def __init__(self):
		self.model = load_model('/home/ccenter/new/17-02-2017_clone/BE/Data/Models/Model1/EnsembleClassifier.h5')
		self.final_probabilities={}

	def returnProbabilities(self,pred_probs):
		encoder=LabelEncoder()
		encoder.classes_ = numpy.load('/home/ccenter/new/17-02-2017_clone/BE/Data/Models/Model1/ensemble.npy')
		print(pred_probs)
		probs = self.model.predict_proba(np.array([pred_probs]),verbose=1)
		print(probs)
		for i in range (10):
			self.final_probabilities[encoder.inverse_transform(i)]=probs[0][i]
		print(self.final_probabilities)
		
		clear_session()
		
	

