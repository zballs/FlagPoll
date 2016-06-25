#!/usr/bin/env python3

# import matplotlib.pyplot as plt
from random import random, randint
from statistics import mode
from operator import add, truediv
from joblib import Parallel, delayed
from math import sqrt

def calcdist(k, data, clusterMembers, contested):
		if k not in clusterMembers and k not in contested:
			dist = 0
			for m in clusterMembers:
				for n in range(len(data[m])):
					dist += (data[m][n]-data[k][n]) ** 2
			dist = dist / len(clusterMembers)
			return (k, dist)
		return (k, float("inf"))


def Classify(data, clusterIds, D):

	closest = float("inf")

	# Iterate through cluster groups
	for i in set(clusterIds):

		clusterMembers = []
		# Get cluster members
		for j in range(len(data)):
			if i == clusterIds[j]:
				clusterMembers.append(j)

		if not clusterMembers:
			continue

		dist = 0
		# Find sum of squared distances to cluster members
		for m in clusterMembers:
			M = data[m]
			for n in range(len(M)):
				dist += (M[n]-D[n]) ** 2

		dist = dist / len(clusterMembers)

		# If closest, change closest and cluster id
		if dist < closest:
			closest = dist
			clust = i

	return clust 

def Merge(data, clusterIds):
    
	# Iterate through clusters
	closest = float("inf")
	for i in set(clusterIds):
		clusterMembers = []

		# Get cluster members
		for j in range(len(data)):
			if i == clusterIds[j]:
				clusterMembers.append(j)

		# Find two closest cluster members overall
		for m in clusterMembers:
			M = data[m]
			for n in clusterMembers:
				if m != n:
					N = data[n]
					dist = 0
					for dim in range(len(M)):
						dist += (M[dim]-N[dim]) ** 2
					if dist < closest:
						closest = dist 
						_m = m
						_n = n
	# Add their featuresets together, insert in first member's data
	data[_m] = [el/2 for el in list(map(add,data[_m],data[_n]))]

	# Delete second member's data and clusterId
	del data[_n]
	del clusterIds[_n]

	return data, clusterIds


# Contested Agglomerative Prototyping
def main():
	open_featsets = ("featsets.pickle","rb")
	data = pickle.load(open_featsets)
	open_featsets.close()

	# Set terminal number of clusters 
	minClusters = 6

	# Create list of Cluster IDs 
	clusterIds = [Id for Id in range(len(data))]

	# Keep track of # iterations
	iters = 1

	# Create list for contested points
	contested = []

	# Initial number of clusters 
	prevNumClusters = len(set(clusterIds))
	prevIterClusters = len(set(clusterIds))

	# Create dict for intra cluster similarities
	intraClusterSims = {}

	# Set number of nearest neighbors for contested points in cluster selection
	numNeighbors = int(len(data) ** 0.5)

	# Create lists for plot data 
	# X = []
	# Y = []
	
	while len(set(clusterIds)) > minClusters:

		# Create Nearest Neighbors and Distances dictionaries
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

			closest = float("inf")

			########## NEAREST POINT METHOD ##########
			# Find Nearest Neighbor to Cluster Group using average link method
			for iteration in range(iters):
				# for k in range(len(data)):
				# 	# Examine data example if not in cluster members and uncontested
				# 	if k not in clusterMembers and k not in contested:
				# 		K = data[k]
				# 		dist = 0

				# 		# Iterate through cluster members, calculate average link distance
				# 		for m in clusterMembers:
				# 			M = data[m]
				# 			for n in range(len(M)):
				# 				dist += (M[n]-K[n]) ** 2
						
				# 		dist = dist / len(clusterMembers)
	                    
	   #                  #  If it's closest, make it nearest point finalist
				# 		if dist < closest:
				# 			nn = k
				# 			closest = dist
				clustdists = Parallel(n_jobs=-1)(delayed(calcdist)(k,data,clusterMembers,contested) for k in range(len(data)))
				closest = min(tup[1] for tup in clustdists)
				for tup in clustdists:
					if tup[1] == closest:
						nn = tup[0]
						break
				
				# If finalist is already in nearest points dict, do cluster face-off
				if nn in nearestNeighbors.keys():
					sumDist = nearestNeighbors[nn] + closest 

					prob1 = (nearestNeighbors[nn] / sumDist) ** iters
					prob2 = closest / sumDist

					rand1 = random()
					rand2 = random()

					cond1 = prob1 < rand1 
					cond2 = prob2 < rand2
					# New cluster wins face-off and finalist joins cluster
					if not cond1 and cond2:
						# Insert NN, Closest in Nearest Neighbor Dict
						nearestNeighbors[nn] = closest
						# Change NN Cluster ID
						clusterIds[nn] = i
						# Append NN to Cluster members list
						clusterMembers.append(nn)
						break

					# Result of face-off is a tie
					elif cond1 and cond2:
						distances = {}
						clustIds = []
						NN = data[nn]
						for g in range(len(data)):
							distances[g] = 0
							G = data[g]
							for h in range(len(NN)):
								distances[g] += (NN[h]-G[h]) ** 2
						for nbr in range(numNeighbors):
							minDist = min(distances.values())
							for d in distances:
								if distances[d] == minDist:
									break
							clustIds.append(clusterIds[d])
							del distances[d]
						# Find X nearest neighbors to finalist, joins most common cluster
						try:
							clusterIds[nn] = mode(clustIds)
						# No mode, add finalist to list of contested points
						except:
							contested.append(nn)

				else:
					# Insert NN, Closest in Nearest Neighbor Dict
					nearestNeighbors[nn] = closest
					# Change NN Cluster ID
					clusterIds[nn] = i
					# Append NN to cluster members list
					clusterMembers.append(nn)
					break

			# Calculate spread of cluster
			spread = 0
			if len(clusterMembers) > 1:
				for l in range(len(clusterMembers)):
					p1 = data[clusterMembers[l]]
					for j in range(l+1, len(clusterMembers)):
						p2 = data[clusterMembers[j]]
						for idx in range(len(p1)):
							spread += (p1[idx]-p2[idx]) ** 2
				intraClusterSims[i] = sqrt(spread) / (len(clusterMembers) * (len(clusterMembers)-1) / 2)

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

		# Assign contested points to clusters... 
		if contested and len(set(clusterIds)) > minClusters: 
			for p in contested:
				try:
					P = data[p]
					distances = {}
					ids = []
				except:
					# if idx out of range, remove from contested list and continue
					contested.remove(p)
					continue

				# Calculate distances from point to uncontested points
				for q in range(len(data)):
					if q not in contested:
						dist = 0
						Q = data[q]
						for r in range(len(P)):
							dist += (P[r] - Q[r]) ** 2
						distances[q] = dist

				# Get cluster ids for X nearest neighbors
				for s in range(numNeighbors):
					minDist = min(distances.values())
					for d in distances:
						if distances[d] == minDist:
							break
					ids.append(clusterIds[d])
					del distances[d]

				# Cluster id of contested point = mode of ids list
				try: 
					clusterIds[p] = mode(ids)
					contested.remove(p)
				except:
					pass

			if prevIterClusters == len(set(clusterIds)):
				data, clusterIds = Merge(data,clusterIds)
			prevIterClusters = len(set(clusterIds))

		iters += 1

	# Plot total spread
	# plt.plot(X,Y)
	# plt.xlabel('number of clusters')
	# plt.ylabel('total spread')
	# plt.show()

	# Return Cluster IDs
	return clusterIds, total






