import sys
import math

class BestAttr(object):
	def __init__(self):
		self.total = 0 # total number of data
		self.attr = [] # list of all attributes (not include target attribute)
		self.data = [] # data (in vertical format)
		self.info_gain = {} # dictionary of info_gain if we select any attribute
		self.gain_ratio = {} # dictionary of info_gain if we select any attribute

		self.info_before = 0 # information of all data before classification

	# read input from stdin 
	def read_input(self):
		message = sys.stdin.readlines()
		# read total # of data
		self.total = int(message[0].rstrip()) - 1
		# read list of attributes
		self.attr = message[1].rstrip().split(',')
		del self.attr[-1] # delete the target label name
		# allocate empty lists for each attribute and the target attribute
		for i in range(len(self.attr)+1):
			self.data.append([])
		
		# convert input data to vertical format and store in self.data
		for i in range(2, len(message)):
			line = message[i].rstrip().split(',')
			for j in range(len(line)):
				self.data[j].append(line[j])

		# print("total:", self.total)
		# print("attr:", self.attr)
		# for i in self.data:
		# 	print(i)

	# use all attributes to classify the data and calculate info_gain and info_ratio
	def calculate(self):
		# i = index of attribute we are investigating now
		for i in range(len(self.attr)):
			# print("attribute:", self.attr[i])
			# number of distinct values of the current attribute
			nb_cluster = len(set(self.data[i])) 
			# dictionary of all distinct values
			cluster = dict()

			# j = index of data
			# form clusters: loop over all data and put the indices of them to correct dictionary
			for j in range(self.total):
				if self.data[i][j] in cluster:
					cluster[self.data[i][j]].append(j)
				else:
					cluster[self.data[i][j]] = [j]


			# print(cluster)

	def find_info_before(self):
		target_idx = len(self.attr)
		# build list of target values
		target_vals = dict()
		# put the number of each value in dictionary
		for i in range(self.total):
			if self.data[target_idx][i] in target_vals:
				target_vals[self.data[target_idx][i]] += 1
			else:
				target_vals[self.data[target_idx][i]] = 1
		# print(target_vals)
		
		# calculate info
		for key in target_vals:
			self.info_before -= (target_vals[key] / self.total) * math.log2(target_vals[key] / self.total)







def main():
	a = BestAttr()
	a.read_input()
	a.calculate()

if __name__ == "__main__": 
	main()

