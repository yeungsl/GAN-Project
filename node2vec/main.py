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


# Read the data into a list of strings.
def read_data(filename):
  """Extract the file and convert it into a neighbor list"""
  BFSlist = {}
  Edgelist = []
  for line in open(filename):
    s, d = line.split(" ")
    src = int(s)
    dst = int(d)
    Edgelist.append((src, dst))
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
  return BFSlist, Edgelist

################# main code ###########################################
start = time.time()
filename = sys.argv[1]
BFSlist, Edgelist = read_data(filename)
#print(BFSlist)
#print(Edgelist)
#print('Adjacent list size', len(BFSlist))
print('edge list size', len(Edgelist))
T = linking_test.Test(BFSlist, Edgelist, float(sys.argv[2]))
Removelist, New_BFSlist, New_Edgelist = T.sample()
#print (Removelist)
#print (New_Edgelist)
#print (New_BFSlist.keys())
#New_BFSlist, New_Edgelist = T.generate_list(Removelist)
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
#print(words)

L = Word2Vec.Learn(words)
matrix, mapping = L.train()

percentage = T.run_test(Removelist, matrix, mapping)
print("the correct rate of prediction is %f "%percentage)

print("Total time comsumed %fs" %(time.time()-start))
