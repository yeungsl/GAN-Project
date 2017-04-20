#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import Word2Vec
import Node2Vec
import random, collections, itertools, copy



def read_data(filename):
    """Extract the file and convert it into a neighbor list"""

    BFSlist = {}
    Edgelist = []
    for line in open(filename):
        (s, d) = line.split(' ')
        #(s,d) = line.split('\t')
        src = s
        dst = d.split('\n')[0]
        Edgelist.append((src, dst))
        BFSlist = BFS(src, dst, BFSlist)

    return (BFSlist, Edgelist)


def BFS(src, dst, BFSlist):
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
    return BFSlist


class Test:

    def __init__(
        self,
        BFSlist,
        Edgelist,
        p,
        ):
        self.E = Edgelist
        self.B = BFSlist
        self.p = p

    def sample(self):
        Edgelist = self.E
        BFSlist = self.B
        p = self.p
        Removelist = []
        New_Edgelist = []
        New_BFSlist = copy.deepcopy(BFSlist)

        for edge in Edgelist:
            r = random.random()
            if r < p:
                if len(New_BFSlist[edge[0]]) == 1 or len(New_BFSlist[edge[1]])  == 1:
                    New_Edgelist.append(edge)
                    continue
                Removelist.append(edge)
                del New_BFSlist[edge[0]][edge[1]]
                del New_BFSlist[edge[1]][edge[0]]
            else:
                New_Edgelist.append(edge)

        return (Removelist, New_BFSlist, New_Edgelist)

    def check(self, src, dst):
        mapping = self.MP
        matrix = self.M

        r = np.linalg.norm(matrix[mapping[src]] - matrix[mapping[dst]])
        return r

    def run_test(
        self,
        Removelist,
        matrix,
        mapping,
        Original_list,
        ):
        self.M = matrix
        self.MP = mapping

        p = self.p
        result = {}
        s = 0
        node_list = set([node for edge in Removelist for node in edge])
        #print(node_list)
        for edge in itertools.combinations(node_list, 2):
            dist = self.check(edge[0], edge[1])
            s += dist
            result[edge] = dist

        normalized_result = {}
        for e in result:
            normalized_result[e] = result[e] / s

        sorted_result = \
            collections.OrderedDict(sorted(normalized_result.items(),
                                    key=lambda t: t[1]))

        n = len(normalized_result) * p
        correct = 0
        count = 1
        print ('getting the first ', n)

        for edge in sorted_result:

            if edge[1] in Original_list[edge[0]].keys() or edge[0]\
                 in Original_list[edge[0]].keys():

                correct += 1
            count += 1
            if count > n:
                break
        print ('correct', correct)

        AUC = (correct * 0.5 + n - correct) / n
        return (correct / n, AUC)


