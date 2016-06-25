#!/usr/bin/env python3

# import matplotlib.pyplot as plt
from joblib import Parallel, delayed

def calcdist(i,j,data,clusterIds,clusterMembers):
	if i != j:
		cluster2Members = []
		dist = 0
		for k in range(len(data)):
			if j == clusterIds[k]:
				cluster2Members.append(k)
		if not cluster2Members:
			return (None,float("inf"))
		for m in clusterMembers:
			for n in cluster2Members:
				for idx in range(len(data[m])):
					dist += (data[m][idx]-data[n][idx])**2
		dist /= (len(clusterMembers) * len(cluster2Members))
		return (cluster2Members,dist)
	return (None,float("inf"))


def main():

	open_featsets = open("featsets.pickle","rb")
	data = pickle.load(open_featsets)
	open_featsets.close()

	# Set terminal number of clusters 
	minClusters = 6

	# Create list of Cluster IDs 
	clusterIds = [Id for Id in range(len(data))]

	# Initial number of clusters 
	prevNumClusters = len(set(clusterIds))

	# Create dict for intra cluster similarities
	intraClusterSims = {}

	# Create lists for plot data 
	# X = []
	# Y = []
	
	while len(set(clusterIds)) > minClusters:

		# Create Nearest Neighbors dict
		nearestNeighbors = {}
		
		# Iterate through Cluster Groups
		for i in set(clusterIds):

			# Create Cluster Members list
			clusterMembers = []

			# Find indexes of Cluster Members
			for j in range(len(data)):
				if i == clusterIds[j]:
					clusterMembers.append(j)

			# If no cluster members, continue to next cluster group
			if not clusterMembers:
				intraClusterSims[i] = 0
				continue

			########## NEAREST CLUSTER METHOD ##########
            # Iterate through other clusters to find nearest one
			clustdists = Parallel(n_jobs=-1)(delayed(calcdist)(i,j,data,clusterIds,clusterMembers) for j in set(clusterIds))
			closest = min(tup[1] for tup in clustdists)
			for tup in clustdists:
				if tup[1] == closest:
					nclustMembers = tup[0]
				
			# Change cluster ids for nclust members 
			for n in nclustMembers:
				clusterIds[n] = i

			# Expand cluster members list 
			clusterMembers += nclustMembers

			# Calculate spread of cluster
			spread = 0
			if len(clusterMembers) > 1:
				for l in range(len(clusterMembers)):
					p1 = data[clusterMembers[l]]
					for j in range(l+1, len(clusterMembers)):
						p2 = data[clusterMembers[j]]
						for idx in range(len(p1)):
							spread += (p1[idx]-p2[idx]) ** 2
				intraClusterSims[i] = spread / (len(clusterMembers) * (len(clusterMembers)-1) / 2)

			# Compute sum of intra cluster similarities 
			total = 0
			for c in intraClusterSims:
				total += intraClusterSims[c]

			numClusters = len(set(clusterIds))
			if numClusters < prevNumClusters:
				prevNumClusters = numClusters
				print(numClusters)
				# X.append(numClusters)
				# Y.append(total)

			# BREAK if we have Min Clusters or less
			if len(set(clusterIds)) <= minClusters:
			    break

	# Plot total spread
	# plt.plot(X,Y)
	# plt.xlabel('number of clusters')
	# plt.ylabel('total spread')
	# plt.show()

	# Return Cluster IDs
	return clusterIds, total

if __name__ == '__main__':
	main()
