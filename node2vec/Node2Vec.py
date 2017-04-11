# Sailung Yeung
# <yeungsl@bu.edu>
# reference:
# https://github.com/aditya-grover/node2vec/blob/master/src/node2vec.py

import numpy as np
import random


class Graph():
  def __init__(self, BFSlist, Edgelist, p, q):
    self.G = BFSlist
    self.E = Edgelist
    self.p = p
    self.q = q

  def node2vec_walk(self, walk_length, start_node):
    '''
    Simulate a random walk starting from start node.
    '''
    G = self.G
    alias_nodes = self.alias_nodes
    alias_edges = self.alias_edges

    walk = [start_node]

    while len(walk) < walk_length:
      cur = walk[-1]
      cur_nbrs = G[cur].keys()
      if len(cur_nbrs) > 0:
        if len(walk) == 1:
          walk.append(cur_nbrs[alias_draw(alias_nodes[cur][0], alias_nodes[cur][1])])
        else:
          prev = walk[-2]
          next = cur_nbrs[alias_draw(alias_edges[(prev, cur)][0], alias_edges[(prev, cur)][1])]
          walk.append(next)
      else:
        break

    return walk

  def simulate_walks(self, num_walks, walk_length):
    '''
    Repeatedly simulate random walks from each node.
    '''
    G = self.G
    walks = []
    nodes = list(G.keys())

    #print ('Walk iteration:')
    for walk_iter in range(num_walks):
      #print str(walk_iter+1), '/', str(num_walks)
      random.shuffle(nodes)
      for node in nodes:
        walks.append(self.node2vec_walk(walk_length=walk_length, start_node=node))

    return walks


  def get_alias_edge(self, src, dst):
    '''
    Get the alias edge setup lists for a given edge.
    '''
    G = self.G
    p = self.p
    q = self.q

    unnormalized_probs = []
    for dst_nbr in G[dst].keys():
      if dst_nbr == src:
        unnormalized_probs.append(G[dst][dst_nbr]/p)
      elif src in G[dst_nbr].keys():
        unnormalized_probs.append(G[dst][dst_nbr])
      else:
        unnormalized_probs.append(G[dst][dst_nbr]/q)
    norm_const = sum(unnormalized_probs)
    normalized_probs =  [float(u_prob)/norm_const for u_prob in unnormalized_probs]

    return alias_setup(normalized_probs)

  def preprocess_transition_probs(self):
    '''
    Preprocessing of transition probabilities for guiding the random walks.
    '''
    G = self.G
    E = self.E

    alias_nodes = {}
    for node in G.keys():
      unnormalized_probs = [G[node][nbr] for nbr in G[node].keys()]
      norm_const = sum(unnormalized_probs)
      normalized_probs =  [float(u_prob)/norm_const for u_prob in unnormalized_probs]
      alias_nodes[node] = alias_setup(normalized_probs)

    alias_edges = {}

    for edge in E:
      alias_edges[edge] = self.get_alias_edge(edge[0], edge[1])
      alias_edges[(edge[1], edge[0])] = self.get_alias_edge(edge[1], edge[0])

    self.alias_nodes = alias_nodes
    self.alias_edges = alias_edges

    return


def alias_setup(probs):
  '''
  Compute utility lists for non-uniform sampling from discrete distributions.
  Refer to https://hips.seas.harvard.edu/blog/2013/03/03/the-alias-method-efficient-sampling-with-many-discrete-outcomes/
  for details
  '''
  K = len(probs)
  q = np.zeros(K)
  J = np.zeros(K, dtype=np.int)

  smaller = []
  larger = []
  for kk, prob in enumerate(probs):
      q[kk] = K*prob
      if q[kk] < 1.0:
          smaller.append(kk)
      else:
          larger.append(kk)

  while len(smaller) > 0 and len(larger) > 0:
      small = smaller.pop()
      large = larger.pop()

      J[small] = large
      q[large] = q[large] + q[small] - 1.0
      if q[large] < 1.0:
          smaller.append(large)
      else:
          larger.append(large)

  return J, q

def alias_draw(J, q):
  '''
  Draw sample from a non-uniform discrete distribution using alias sampling.
  '''
  K = len(J)

  kk = int(np.floor(np.random.rand()*K))
  if np.random.rand() < q[kk]:
      return kk
  else:
      return J[kk]
