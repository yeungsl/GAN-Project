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
print('Adjacent list size', len(BFSlist))
print('edge list size', len(Edgelist))

# generating all the walks that needed in learning

p = 0.5
q = 0.5
num_walks = 10
walk_length = 80

G = Node2Vec.Graph(BFSlist, Edgelist, p, q)
G.preprocess_transition_probs()
walks = G.simulate_walks(num_walks, walk_length)
print('walk list size', len(walks))
words = []
for walk in walks:
  words.extend([str(step) for step in walk])
#print(words)

L = Word2Vec.Learn(words)
matrix, mapping = L.train()

T = linking_test.Test(BFSlist, Edgelist, matrix, mapping)
Removelist = T.sample()
test1 = T.run_test1(Removelist)
#print(test1)

output = open(sys.argv[2], 'w')
output.write('------------------test1----------------------\n')
for line in test1:
  output.write(str(line) + ' ' + str(test1[line]) + '\n')

if sys.argv[3] == '1':
  #Removelist = T.sample()
  test2 = T.run_test2(Removelist)
  '''
  print('Adjacent list size', len(BFSlist))
  print('edge list size', len(Edgelist))
  
  N_G = Node2Vec.Graph(BFSlist, Edgelist, p, q)
  N_G.preprocess_transition_probs()
  walks = N_G.simulate_walks(num_walks, walk_length)
  print('walk list size', len(walks))
  for walk in walks:
    words.extend([str(step) for step in walk])
  #print(words)

  N_L = Word2Vec.Learn(words)
  matrix, mapping = N_L.train()

  N_T = linking_test.Test(BFSlist, Edgelist, matrix, mapping)
  test2 = N_T.run_test1(Removelist)
  '''
  output.write('-------------------test2-------------------\n')
  for line in test2:
    output.write(str(line) + ' ' + str(test2[line]) + '\n')
output.close()
print("Total time comsumed %fs" %(time.time()-start))
