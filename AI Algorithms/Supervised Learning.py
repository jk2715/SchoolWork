import numpy as np

class KNN:
	def __init__(self, k):
		#KNN state here
		#Feel free to add methods
		self.k = k
		self.X = []
		self.y = []

	def distance(self, featureA, featureB):
		diffs = (featureA - featureB)**2
		return np.sqrt(diffs.sum())

	def train(self, X, y):
		#training logic here
		self.X = X[:]
		self.y = y[:]
		#input is an array of features and labels
		None

	def predict(self, X):
		#Run model here
		labels = []
		predictions = []
		for x1 in X:
			distances = []
			nn = []
			for x2 in self.X:
				distances.append(self.distance(x1, x2))
			tmp = distances[:]
			tmp2 = []
			for i in range(self.k):
				closest = min(tmp)
				nn.append(closest)
				tmp.remove(closest)
				ind = distances.index(closest)
				tmp2.append(self.y[ind])
			labels.append(tmp2)
		for l in labels:
			mode = max(set(l), key = l.count)
			predictions.append(mode)
		#Return array of predictions where there is one prediction for each set of features
		return np.asarray(predictions)


class Perceptron:
	def __init__(self, w, b, lr):
		#Perceptron state here, input initial weight matrix
		#Feel free to add methods
		self.lr = lr
		self.w = w
		self.b = b
		self.X = []
		self.y = []
		self.steps = 0

	def train(self, X, y, steps):
		#training logic here
		self.X = X[:]
		self.y = y[:]
		self.steps = steps
		#input is array of features and labels
		None

	def predict(self, X):
		#Run model here
		test_pred = []
		for s in range(self.steps):
			prediction = -1
			n = np.random.randint(len(self.y))
			if np.dot(np.transpose(self.w), self.X[n]) + self.b * 1 > 0:
				prediction = 1
			else:
				prediction = 0
			if prediction != self.y[n]:
				self.w += self.lr * (self.y[n] - prediction) * self.X[n]
				self.b += self.lr * (self.y[n] - prediction) * 1
		for i in range(len(X)):
			if np.dot(np.transpose(self.w), X[i]) + self.b * 1 > 0:
				test_pred.append(1)
			else:
				test_pred.append(0)
		#Return array of predictions where there is one prediction for each set of features
		return np.asarray(test_pred)


class MLP:
	def __init__(self, w1, b1, w2, b2, lr):
		self.l1 = FCLayer(w1, b1, lr)
		self.a1 = Sigmoid()
		self.l2 = FCLayer(w2, b2, lr)
		self.a2 = Sigmoid()

	def MSE(self, prediction, target):
		return np.square(target - prediction).sum()

	def MSEGrad(self, prediction, target):
		return - 2.0 * (target - prediction)

	def shuffle(self, X, y):
		idxs = np.arange(y.size)
		np.random.shuffle(idxs)
		return X[idxs], y[idxs]

	def train(self, X, y, steps):
		for s in range(steps):
			i = s % y.size
			if(i == 0):
				X, y = self.shuffle(X,y)
			xi = np.expand_dims(X[i], axis=0)
			yi = np.expand_dims(y[i], axis=0)

			pred = self.l1.forward(xi)
			pred = self.a1.forward(pred)
			pred = self.l2.forward(pred)
			pred = self.a2.forward(pred)
			loss = self.MSE(pred, yi) 
			#print(loss)

			grad = self.MSEGrad(pred, yi)
			grad = self.a2.backward(grad)
			grad = self.l2.backward(grad)
			grad = self.a1.backward(grad)
			grad = self.l1.backward(grad)

	def predict(self, X):
		pred = self.l1.forward(X)
		pred = self.a1.forward(pred)
		pred = self.l2.forward(pred)
		pred = self.a2.forward(pred)
		pred = np.round(pred)
		return np.ravel(pred)

class FCLayer:

	def __init__(self, w, b, lr):
		self.lr = lr
		self.w = w	#Each column represents all the weights going into an output node
		self.b = b
		self.a = []

	def forward(self, input):
		#Write forward pass here
		prod = np.dot(np.transpose(self.w), np.transpose(input))
		self.a = np.transpose(prod) + self.b
		return self.a

	def backward(self, gradients):
		#Write backward pass here
		deriv = gradients[0]
		d1 = gradients[1]
		b = []
		prod = np.dot(self.w, d1)
		delta = prod * deriv
		self.w -= self.lr * self.a * delta
		self.b -= self.lr * delta[0][0]
		return delta

class Sigmoid:

	def __init__(self):
		self.input = []
		None

	def forward(self, input):
		#Write forward pass here
		self.input = input
		return 1.0/(1.0 + np.exp(-input))

	def backward(self, gradients):
		#Write backward pass here
		deriv = self.forward(self.input) * (1 - self.forward(self.input))
		return 	deriv, deriv * gradients