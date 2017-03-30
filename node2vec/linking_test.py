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
    def run_test1(self, Removelist):
    	result = {}
    	s = 0
    	for edge in Removelist:
    		dist = self.check(edge[0], edge[1])
    		s += dist
    		result[edge] = dist
    	normalized_result = {}
    	for e in result:
    		normalized_result[e] = result[e]/s
    	
    	return collections.OrderedDict(sorted(normalized_result.items(), key=lambda t:t[1]))
    def run_test2(self, Removelist):
        Edgelist = self.E
        New_Edgelist = []
        BFSlist = {}    
        for edge in Edgelist:
            if edge not in Removelist:
                src = edge[0]
                dst = edge[1]
                New_Edgelist.append((src, dst))
                if src not in BFSlist.keys():
                  BFSlist[src] = {dst: 1}
                  if dst not in BFSlist.keys():
                    BFSlist[dst] = {src: 1}
                  else:
                    BFSlist[dst].update({src: 1})
                else:
                  BFSlist[src].update({dst: 1})
                  if dst not in BFSlist.keys():
                    BFSlist[dst] = {src: 1}
                  else:
                    BFSlist[dst].update({src: 1})
        return BFSlist, New_Edgelist
        