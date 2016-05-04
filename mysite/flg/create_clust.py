import random
import pickle
import nltk
from flg.agg_clust import AgglomerativeClustering

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
clust = AgglomerativeClustering(featsets, 6)

# Variable containing unique cluster id values
clust_ids = set(clust)

# Initialize empty cluster features dictionary
clust_feats = {}

# Iterate through cluster groups to get 'True' features
for c in clust_ids:
	true_feats = []
	for index in range(len(clust)):
		if c == clust[index]:
			this_featset = featsets[index]
			for ID in range(len(all_feats)):
				if this_featset[ID]:
					true_feats.append(all_feats[ID])

	# Create frequency distribution of 'True' features
	true_feats = nltk.FreqDist(true_feats)

	# Add frequency distribution to cluster features dictionary
	clust_feats[c] = true_feats

# Save clustering
save_clust = open("clust.pickle","wb")
pickle.dump(clust, save_clust)
save_clust.close()

# Save cluster features
save_clust_feats = open("clust_feats.pickle","wb")
pickle.dump(clust_feats, save_clust_feats)
save_clust_feats.close()

# Save feature sets to preserve ordering
save_featsets = open("featsets.pickle","wb")
pickle.dump(featsets, save_featsets)
save_featsets.close()

# Save word and bigram features to preserve ordering
save_all_feats = open("all_feats.pickle","wb")
pickle.dump(all_feats, save_all_feats)
save_all_feats.close()