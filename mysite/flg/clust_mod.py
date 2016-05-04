import pickle
import nltk
from flg.create_feats import find_feats
from flg.agg_clust import Classify

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
ClustFeats = open("clust_feats.pickle","rb")
clust_feats = pickle.load(ClustFeats)
ClustFeats.close()

def Cluster(d, topNumber):
	clust_id = Classify(featsets, clust, d)
	these_feats = clust_feats[clust_id]
	top_feats = [i[0] for i in these_feats.most_common(topNumber)]
	return clust_id, top_feats
