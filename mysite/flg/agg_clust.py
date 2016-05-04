def AgglomerativeClustering(data, minClusters):

	# Create list of Cluster IDs 
	clusterIds = [Id for Id in range(len(data))]
	
	while len(set(clusterIds)) > minClusters:

		# Create Nearest Neighbors list
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
				continue

			closest = float("inf")
            
			# Find Nearest Neighbor to Cluster Group
			for k in range(len(data)):

				if k not in clusterMembers:
					K = data[k]
					dist = 0

					for m in clusterMembers:
						M = data[m]
						for n in range(len(M)):
							dist += (M[n]-K[n]) ** 2
					
					dist = dist / len(clusterMembers)
                    
					if dist < closest:
						if k not in nearestNeighbors.keys():
							nn = k
							closest = dist
						else:
							if dist < nearestNeighbors[k]:
								nn = k
								closest = dist

			# Append (NN, Closest) to Nearest Neighbor Dict
			nearestNeighbors[nn] = closest

			# Change NN Cluster ID
			clusterIds[nn] = i
			
			# BREAK if we have Min Clusters or less
			if len(set(clusterIds)) <= minClusters:
			    break

	# Return Cluster IDs
	return clusterIds


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

