#!/usr/bin/env python3

import pickle
import csv
import nltk
from statistics import mode
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from operator import truediv
from math import log
from copy import deepcopy
from featsets import featfreqs 

with open("testitems.csv") as file:
    reader = csv.reader(file)
    item_list = list(reader)
item_list = item_list[1:]

ratings = [item[0] for item in item_list]
reviews = [item[1] for item in item_list]

open_word_feats = open("word_feats.pickle","rb")
word_feats = pickle.load(open_word_feats)
open_word_feats.close()

open_bigram_feats = open("bigram_feats.pickle","rb")
bigram_feats = pickle.load(open_bigram_feats)
open_bigram_feats.close()

open_trigram_feats = open("trigram_feats.pickle","rb")
trigram_feats = pickle.load(open_trigram_feats)
open_trigram_feats.close()

open_docfreqs = open("docfreqs.pickle","rb")
docfreqs = pickle.load(open_docfreqs)
open_docfreqs.close()

open_featsets = open("featsets.pickle","rb")
featsets = pickle.load(open_featsets)
open_featsets.close()

open_testratings = open("testratings.pickle","rb")
testratings = pickle.load(open_testratings)
open_testratings.close()

open_gnb = open("gnb.pickle","rb")
gnb = pickle.load(open_gnb)
open_gnb.close()

open_knn = open("knn.pickle","rb")
knn = pickle.load(open_knn)
open_knn.close()

open_svc = open("svc.pickle","rb")
svc = pickle.load(open_svc)
open_svc.close()

def vote(testsets,*classifiers):
	predictions = {}
	for idx, classifier in enumerate(classifiers):
		predictions[idx] = classifier.predict(testsets)
	output = []
	for idx in range(len(testsets)):
		temp = []
		for key in predictions:
			temp.append(predictions[key][idx])
		output.append(mode(temp))
	return output, testsets

def accuracy(predictions,targets):
	if len(predictions) != len(targets):
		print("Number of predictions does not equal number of targets")
	count = 0
	for idx, prediction in enumerate(predictions):
		if prediction == targets[idx]:
			count += 1
	accuracy = float(count / len(predictions))
	return accuracy

testsets = [list(map(truediv,featfreqs(review),docfreqs)) for review in reviews]

gnb_predictions = gnb.predict(testsets)
gnb_accuracy = gnb.score(testsets,testratings)
print('GaussianNB accuracy: %d' % gnb_accuracy)

knn_predictions = knn.predict(testsets)
knn_accuracy = knn.score(testsets,testratings)
print('KNeighbors accuracy: %d' % knn_accuracy)

svc_predictions = svc.predict(testsets)
svc_accuracy = svc.score(testsets,testratings)
print('SVC accuracy: %d' % svc_accuracy)

votes = vote(testsets,gnb,knn,svc)
vote_accuracy = accuracy(votes,testratings)
print('Vote accuracy: %d' % vote_accuracy)



