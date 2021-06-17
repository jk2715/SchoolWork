import numpy as np
import math

class K_MEANS:

	def __init__(self, k, t):
		#k_means state here
		#Feel free to add methods
		# t is max number of iterations
		# k is the number of clusters
		self.k = k
		self.t = t
		self.cluster = []

	def distance(self, centroids, datapoint):
		diffs = (centroids - datapoint)**2
		return np.sqrt(diffs.sum(axis=1))

	def train(self, X):
		#training logic here
		k_means = X[np.random.choice(X.shape[0], self.k, replace = False), :]
		clusters = []
		for x in X:
			clusters.append([0, x])
		for t in range(self.t):
			for i in range(len(X)):
				dist = self.distance(k_means, X[i])
				closest = min(dist)
				ind = np.where(dist == closest)
				clusters[i][0] = ind[0]
			for i in range(len(k_means)):
				points =[]
				for c in clusters:
					if c[0] == i:
						points.append(c[1])
				k_means[i] = np.mean(points, axis=0)
		#input is array of features (no labels)
		self.cluster = clusters

		return self.cluster
		#return array with cluster id corresponding to each item in dataset


class AGNES:
	#Use single link method(distance between cluster a and b = distance between closest
	#members of clusters a and b
	def __init__(self, k):
		#agnes state here
		#Feel free to add methods
		# k is the number of clusters 
		self.k = k

	def distance(self, a, b):
		diffs = (a - b)**2
		return np.sqrt(diffs.sum())

	def train(self, X):
		#training logic here
		#input is array of features (no labels)
		cluster_n = 0
		clusters = []
		for i in range(len(X)):
			clusters.append([i, X[i]])
		while cluster_n != self.k:
			added = []
			for i in range(len(X)):
				if any(np.array_equal(X[i], a) for a in added):
					continue
				dist = []
				pairs = []
				for j in range(len(X)):
					if clusters[i][0] != clusters[j][0]:
						dist.append(self.distance(clusters[i][1], clusters[j][1]))
						pairs.append([clusters[i][0], clusters[j][0]])
				closest = min(dist)
				ind = dist.index(closest)
				for i in range(len(clusters)):
					if clusters[i][0] == pairs[ind][1]:
						added.append(clusters[i][1])
						clusters[i][0] = pairs[ind][0]
						ids = np.asarray([row[0] for row in clusters])
						vals, indices = np.unique(ids, return_index=True)
						cluster_n = len(indices)
					if cluster_n == self.k:
						break
		ids = np.asarray([row[0] for row in clusters])
		vals, indices = np.unique(ids, return_index=True)
		for i in range(len(clusters)):
			indx = np.where(vals == clusters[i][0])
			clusters[i][0] = indx[0]
		self.cluster = clusters
		return self.cluster



		#return array with cluster id corresponding to each item in dataset

