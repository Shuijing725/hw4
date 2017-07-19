import sys
import math

class BestAttr(object):
	def __init__(self):
		self.total = 0 # total number of data
		self.attr = [] # list of all attributes (not include target attribute)
		self.data = [] # data (in vertical format)

		self.info_gain = dict() # dictionary of info_gain if we select any attribute
		self.gain_ratio = dict() # dictionary of info_gain if we select any attribute
		# self.target_vals = dict() # dictionary of all possible target attribute values with number of data in it
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
		# calculate info_before
		self.find_info_before()
		# i = index of attribute we are investigating now
		for i in range(len(self.attr)):
			# print("attribute:", self.attr[i])
			# number of distinct values of the current attribute
			# nb_cluster = len(set(self.data[i])) 

			# dictionary of all distinct values (key: values of current attribute, val: indices of data with attr value = key)
			cluster = dict()

			# j = index of data
			# form clusters: loop over all data and put the indices of them to correct dictionary
			for j in range(self.total):
				if self.data[i][j] in cluster:
					cluster[self.data[i][j]].append(j)
				else:
					cluster[self.data[i][j]] = [j]

			# calculate info_gain for the current cluster
			self.find_info_gain_ratio(cluster, self.attr[i])
			# print(cluster)

		# compare info_gain and info_gain_ratio for all classifications and select the best one
		info_gain_max = max(self.info_gain, key = self.info_gain.get)
		gain_ratio_max = max(self.gain_ratio, key = self.gain_ratio.get)
		print(info_gain_max)
		print(gain_ratio_max)
			

	# calculate self.info_before
	def find_info_before(self):
		target_idx = len(self.attr)
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
		# print('info_before:', self.info_before)


	# calculate infomation gain for each cluster to fill in self.info_gain
	def find_info_gain_ratio(self, cluster, attribute):
		# print("")
		# print("find info gain ratio with attribute = ", attribute)
		# print("cluster = ", cluster)

		self.info_gain[attribute] = 0

		# ret_val = dict() 
		target_idx = len(self.attr)
		split_info = 0
		info_after = 0 # stores information after classification

		# loop through all keys in cluster to find info after clustering
		for key, val in cluster.items():
			# print('examine key =', key, 'val = ', val)
			ret_val = dict() 
			info_after_each = 0  # information for each cluster after classification
			split_info -= (len(val) / self.total) * math.log2(len(val) / self.total)
			# for all indices of data in current key
			for i in val:
				if self.data[target_idx][i] in ret_val:
					ret_val[self.data[target_idx][i]] += 1
				else:
					ret_val[self.data[target_idx][i]] = 1

			# print('ret_val = ', ret_val)
			# find info gain of ret_val
			for key1 in ret_val:
				info_after_each -= (ret_val[key1] / len(val)) * math.log2(ret_val[key1] / len(val))
			info_after += (len(val) / self.total) * info_after_each
			# print("info_after_each:", info_after_each)

		self.info_gain[attribute] = self.info_before - info_after
		self.gain_ratio[attribute] = self.info_gain[attribute] / split_info
		# print('info after:', info_after)
		# print('info_gain:', self.info_gain[attribute])

def main():
	a = BestAttr()
	a.read_input()
	a.calculate()

if __name__ == "__main__": 
	main()

