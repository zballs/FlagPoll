import pickle
import nltk
import create_clust # run clustering
from create_feats import find_feats
from agg_clust import Classify

# Retrieve feature sets
FeatSets = open("featsets.pickle","rb")
featsets = pickle.load(FeatSets)
FeatSets.close()

# Retrieve word and bigram features
AllFeats = open("all_feats.pickle","rb")
all_feats = pickle.load(AllFeats)
AllFeats.close()

# Retrieve clustering
Clust = open("clust.pickle","rb")
clust = pickle.load(Clust)
Clust.close()

# Retrieve cluster features
Labels = open("labels.pickle","rb")
labels = pickle.load(Labels)
Labels.close()

def whichCluster(text):
	featset = find_feats(text)
	clust_id = Classify(featsets, clust, featset)
	return clust_id, labels[clust_id]
