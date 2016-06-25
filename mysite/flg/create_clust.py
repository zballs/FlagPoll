#!/usr/bin/env python3

import random
import pickle
import nltk
import create_feats # run featureset creation 
from operator import add, truediv

# Retrieve feature sets
FeatSets = open("featsets.pickle","rb")
featsets = pickle.load(FeatSets)
FeatSets.close()

# Retrieve word and bigram features
AllFeats = open("all_feats.pickle","rb")
all_feats = pickle.load(AllFeats)
AllFeats.close()

# Shuffle featsets
random.shuffle(featsets)

# Implement clustering, get cluster id values
clust, total_spread = MyClustering(featsets, 6)
clust, total_spread = AgglomerativeClustering(featsets, 6)


# Variable containing unique cluster id values
clust_ids = set(clust)

# Initialize feature frequencies, scores, and labels dictionaries
all_freqs = {}
total_freq = [0 for feat in all_feats]
score_sets = {}
labels = {}
threshold = 0.5 # higher number for more selective label assignment

# Iterate through cluster groups to determine appropriate labels
for c in clust_ids:
	freq = [0 for feat in all_feats]

	for index in range(len(clust)):
		if c == clust[index]:
			# Calculate feature frequencies by cluster
			freq += list(map(add,featsets[index],freq))
	# Store in all freqs dict
	all_freqs[c] = freq

	# Calculate total feature frequencies
	total_freq += list(map(add,total_freq,freq))

# Calculate feature scores by cluster (fraction of total feature freqs)
for c in clust_ids:
	freq = all_freqs[c]
	score_sets[c] = list(map(truediv,freq,total_freq))

for c in clust_ids:
	score_set = score_sets[c]
	for index in range(len(score_set)):
		# If feature score is over threshold, add to cluster labels 
		if score_set[index] > threshold:
			if not labels[c]:
				labels[c] = []
			labels[c].append(all_feats[index])


# Save clustering
save_clust = open("clust.pickle","wb")
pickle.dump(clust, save_clust)
save_clust.close()

# Save cluster labels
save_labels = open("labels.pickle","wb")
pickle.dump(labels, save_labels)
save_labels.close()

# Save feature sets to preserve ordering
save_featsets = open("featsets.pickle","wb")
pickle.dump(featsets, save_featsets)
save_featsets.close()

# Save word and bigram features to preserve ordering
save_all_feats = open("all_feats.pickle","wb")
pickle.dump(all_feats, save_all_feats)
save_all_feats.close()