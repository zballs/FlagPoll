import pickle
import csv
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from operator import truediv
from math import log
from copy import deepcopy
from create_feats import featfreqs

with open("testitems.csv") as file:
	reader = csv.reader(file)
	item_list = list(reader)
item_list = item_list[1:]

open_featsets = open("featsets.pickle","rb")
featsets = pickle.load(open_featsets)
open_featsets.close()

open_docfreqs = open("docfreqs.pickle","rb")
docfreqs = pickle.load(open_docfreqs)
open_docfreqs.close()

open_word_feats = open("word_feats.pickle","rb")
word_feats = pickle.load(open_word_feats)
open_word_feats.close()

open_bigram_feats = open("bigram_feats.pickle","rb")
bigram_feats = pickle.load(open_bigram_feats)
open_bigram_feats.close()

open_trigram_feats = open("trigram_feats.pickle","rb")
trigram_feats = pickle.load(open_trigram_feats)
open_trigram_feats.close()

open_all_feats = open("all_feats.pickle","rb")
all_feats = pickle.load(open_all_feats)
open_all_feats.close()

open_clustr = open("clustr.pickle","rb")
clustr = pickle.load(open_clustr)
open_clustr.close()

open_sigfeats = open("sigfeats.pickle","rb")
sigfeats = pickle.load(open_sigfeats)
open_sigfeats.close()


testsets = [list(map(truediv,featfreqs(item),docfreqs)) for item in item_list]

labels = set(clustr.labels_)

def characterize(testset):

	distances = {}
	thresholds = {}
	attributes = {}

	# Iterate through cluster groups by label
	for label in labels:

		clusterMembers = []

		# Get cluster members
		for i in range(len(featsets)):
			if label == clustr.labels_[i]:
				clusterMembers.append(i)

		if not clusterMembers:
			continue

		dist = 0

		# Find sum of squared distances to cluster members
		for cm in clusterMembers:
			f = featsets[cm]
			for n in range(len(f)):
				dist += (f[n]-testset[n]) ** 2

		dist /= len(clusterMembers)
		distances[label] = dist

	sumdist = 0
	for label in distances:
		sumdist += distances[label]
	for label in distances:
		thresholds[label] = distances[label] / sumdist

	for label in thresholds:
		_sigfeats = sigfeats[label]
		for sigfeat in _sigfeats:
			for idx, feat in enumerate(all_feats):
				if sigfeat == feat and testset[idx] > thresholds[label]:
					if not attributes[label]:
						attributes[label] = []
					attributes[label].append(sigfeat)

	return attributes, distances

output = {}
maxrank = 0
for idx, testset in enumerate(testsets):
	output[idx] = {}
	attributes, distances = characterize(testset)
	if len(attributes) > maxrank:
		maxrank = len(attributes)
	_distances = deepcopy(distances)
	closest = min(distances.values())
	done = False
	rank = 0
	while not done:
		for label in _distances:
			if _distances[label] == closest:
				output[idx][rank] = attributes[label]
				del distances[label]
				if not distances:
					done = True
					break
				closest = min(distances.values())
				rank += 1

ranked_output = {}
for rank in range(maxrank):
	ranked_output[rank] = []
	for idx in outputs:
		try:
			ranked_output[rank] += output[idx][rank]
		except:
			pass

filtered_output = {}
threshold = log(len(testsets))
for rank in ranked_output:
	filtered_output[rank] = []
	rank_attr_freqs = nltk.FreqDist(ranked_output[rank])
	for attr in rank_attr_freqs:
		freq = rank_attr_freqs[attr]
		if freq > threshold:
			filtered_output[rank].append(attr)

save_filtered_output = open("filtered_output.pickle","wb")
pickle.dump(filtered_output, save_filtered_output)
save_filtered_output.close()


