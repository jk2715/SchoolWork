import numpy as np
import math

class ID3:
	def __init__(self, nbins, data_range):
		#Decision tree state here
		#Feel free to add methods
		self.bin_size = nbins
		self.range = data_range
		self.decision_tree = {}
		self.labels = []

	def preprocess(self, data):
		#Our dataset only has continuous data
		norm_data = np.clip((data - self.range[0]) / (self.range[1] - self.range[0]), 0, 1)
		categorical_data = np.floor(self.bin_size*norm_data).astype(int)
		return categorical_data

	def train(self, X, y):
		#training logic here
		#input is array of features and labels
		#stores a decision tree and a label for each outcome of the tree
		#also stores the index of the attribute being split on at each level of the tree
		#decision tree is a dictionary with multiple levels
		categorical_data = self.preprocess(X)
		arr = self.split(categorical_data, y)
		split = arr[0]
		decision_tree = {}
		majority_labels = []
		node = []
		for samples in split:
			node.append([samples[0], samples[1], arr[1]])
		decision_tree.update({1:node})
		levels = decision_tree.keys()
		i = 1
		while i in levels:
			d_items = decision_tree.get(i)
			indices = []
			for item in d_items:
				node = item[0][:]
				arr = self.split(node, item[1])
				next_split = arr[0]
				if len(next_split) == 1:
					mode = max(set(next_split[0][1]), key = next_split[0][1].count)
					majority_labels.append([indices, mode])
				else:
					node = []
					for ns in next_split:
						node.append([ns[0], ns[1], arr[1]])
					indices.append(arr[1])
					decision_tree.update({i+1:node})
			levels = decision_tree.keys()
			i += 1
		self.decision_tree, self.labels = decision_tree, majority_labels
				




	def predict(self, X):
		#Run model here
		#Return array of predictions where there is one prediction for each set of features
		#takes the input and travels down the tree
		#compares the attributes of the input to the attributes of the tree at each level, using the stored indices
		#the path traveled is determined by the indices of matching attributes at each tree level
		#predictions are then made according to the label matching the traveled path
		categorical_data = self.preprocess(X)
		predictions = []
		for i in range(len(X)):
			indices = []
			for k in self.decision_tree.keys():
				eval = False
				for item in self.decision_tree.get(k):
					ind = item[2]
					for value in item[0]:
						if categorical_data[i][ind] == value[ind]:
							eval = True
							for index in indices:
								if categorical_data[i][index] != value[index]:
									eval = False
									break
						if eval:
							indices.append(ind)
							break
					if eval:
						break
			for l in self.labels:
				if(all(x in indices for x in l[0])):
					predictions.append(l[1])
					break
		return np.asarray(predictions)

	def entropy(self, a, b):
		#calculate entropy
		c = a + b
		return -a/c * np.log(a/c) - b/c * np.log(b/c)

	def split(self, X, y):
		#splits the input based on attribute with maximum gain
		#returns an array containing the split rows, along with the index of the attribute being split on
		gains = []
		attr = np.transpose(X)
		y_value = 0
		n_value = 0
		for l in y:
			if l == 0:
				n_value += 1
			else:
				y_value += 1
		entropy_value = self.entropy(y_value, n_value)
		num = len(X)
		for i in range(len(attr)):
			vals = np.unique(attr[i])
			info = 0
			for v in vals:
				yes = 0
				no = 0
				for j in range(num):
					if X[j][i] == v:
						if y[j] == 0:
							no += 1
						else:
							yes += 1
				entropy = self.entropy(yes, no)
				info += ((yes + no)/num) * entropy
			gains.append(entropy_value - info)
		mx =  max(gains)
		ind = gains.index(mx)
		split = []
		column = [row[ind] for row in X]
		unique_vals = np.unique(column)
		for v in unique_vals:
			tmp_x = []
			tmp_y = []
			for i in range(len(X)):
				if X[i][ind] == v:
					tmp_x.append(X[i])
					tmp_y.append(y[i])
			split.append([tmp_x, tmp_y])
		return split, ind