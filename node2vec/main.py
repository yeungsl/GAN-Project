# Sailung Yeung
# <yeungsl@bu.edu>
# reference:
# http://www.cnblogs.com/edwardbi/p/5509699.html

import numpy as np
import Node2Vec
import Word2Vec
import linking_test
import collections, math, os, random, httplib, sys, time

# Read in the same data as used in tensoflow template
# https://github.com/tensorflow/tensorflow/blob/master/tensorflow/examples/tutorials/word2vec/word2vec_basic.py
# for comparasion




################# main code ###########################################
start = time.time()
filename = sys.argv[1]
BFSlist, Edgelist = linking_test.read_data(filename)
print(BFSlist)

print('edge list size', len(Edgelist))
T = linking_test.Test(BFSlist, Edgelist, float(sys.argv[2]))
Removelist, New_BFSlist, New_Edgelist = T.sample()
print('New edge list size', len(New_Edgelist))
# generating all the walks that needed in learning

p = 0.5
q = 0.5
num_walks = 10
walk_length = 80

G = Node2Vec.Graph(New_BFSlist, New_Edgelist, p, q)
G.preprocess_transition_probs()
walks = G.simulate_walks(num_walks, walk_length)
print('walk list size', len(walks))
words = []
for walk in walks:
  words.extend([str(step) for step in walk])


L = Word2Vec.Learn(words)
matrix, mapping = L.train()
print(mapping)
percentage, AUC = T.run_test(Removelist, matrix, mapping, BFSlist)
print("the percetion of prediction is %f "%percentage)
print("the AUC of prediction is %f"%AUC)
print("Total time comsumed %fs" %(time.time()-start))
