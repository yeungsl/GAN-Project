# Sailung Yeung
# <yeungsl@bu.edu>

import numpy as np
import random, collections

class Test():
    def __init__(self, BFSlist, Edgelist, matrix, mapping):
        self.G = BFSlist
        self.E = Edgelist
        self.M = matrix
        self.MP = mapping
    def sample(self):
    	Edgelist = self.E
    	Removelist = []
    	for edge in Edgelist:
    		p = random.random()
    		if p < 0.1:
    			Removelist.append(edge)
    	return Removelist
    def check(self, src, dst):
    	mapping = self.MP
    	matrix = self.M
    	r = np.linalg.norm(matrix[mapping[str(src)]] - matrix[mapping[str(dst)]])
    	return r
    def run_test(self)
    	Removelist = self.sample()
    	result = {}
    	s = 0
    	for edge in Removelist:
    		dist = self.check(edge[0], edge[1])
    		s += dist
    		result[edge] = dist
    	normalized_result = {}
    	for e in result:
    		normalized_result[e] = result[e]/s
    	
    	return collections.OrderedDict(sorted(d.items(), key=lambda t:t[1]))