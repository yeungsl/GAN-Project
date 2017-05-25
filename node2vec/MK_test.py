#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import networkx as nx
import random, collections, itertools, copy, math, os, pickle



class Test:

    def __init__(self, path ,p):
        self.path = path
        self.p = p

    def readG(self):
        path = self.path
        files = os.listdir(path)
        nx_graphs = []
        total_edges = 0
        for name in files:
            if name.endswith(".pickle"):
                print(path+name)
                g = pickle.load(open(path + name, "rb"))
                g_need = max(nx.connected_component_subgraphs(g), key=len)
                nx_graphs.append(g_need)
                total_edges += len(g_need.edges())

        self.G = nx_graphs
        self.n_edges = total_edges

    def sample(self):
        graphs = self.G
        p = self.p
        Removelist = []
        portion = math.ceil((self.n_edges * p)/3)

        for g in graphs:
            shuf_edges = g.edges()
            random.shuffle(shuf_edges)
            for edge in shuf_edges:
                r = random.random()
                if r < p:
                    if len(g.neighbors(edge[0])) == 1 or len(g.neighbors(edge[1]))  == 1:
                        continue
                    Removelist.append(edge)
                    g.remove_edge(*edge)
                if len(Removelist) >= portion:
                    break


        self.rlist = Removelist
        return graphs

    def check(self, src, dst):
        mapping = self.MP
        matrix = self.M
        r = np.linalg.norm(matrix[mapping[src]] - matrix[mapping[dst]])
        return r

    def run_test(self, matrix, mapping, Original_graphs):
        self.M = matrix
        self.MP = mapping
        Removelist = self.rlist
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

        sorted_result = collections.OrderedDict(sorted(normalized_result.items(), key=lambda t: t[1]))

        n = len(normalized_result) * p
        correct = 0
        count = 1
        print ('getting the first ', n)

        for edge in sorted_result:
            in_graph = self.edge_in_graphs(edge, Original_graphs)
            if in_graph:
                correct += 1

            count += 1
            if count > n:
                break
        print ('correct', correct)

        AUC = (correct * 0.5 + n - correct) / n
        return (correct / n, AUC)

    def run_matching_test(self, matrix, mapping, Original_graphs):
        self.M = matrix
        print(len(matrix))
        self.MP = mapping
        p = self.p
        result = {}
        s = 0
        node_list = self.common_nodes(mapping, Original_graphs)
        #print(node_list)
        for edge in itertools.combinations(node_list, 2):
            dist = self.check(edge[0], edge[1])
            s += dist
            result[edge] = dist

        normalized_result = {}
        for e in result:
            normalized_result[e] = result[e] / s

        sorted_result = collections.OrderedDict(sorted(normalized_result.items(), key=lambda t: t[1]))

        n = len(normalized_result) * p
        correct = 0
        count = 1
        print ('getting the first ', n)

        for edge in sorted_result:
            in_graph = self.edge_in_graphs(edge, Original_graphs)
            if in_graph:
                correct += 1

            count += 1
            if count > n:
                break
        print ('correct', correct)

        AUC = (correct * 0.5 + n - correct) / n
        return (correct / n, AUC)

    def edge_in_graphs(self, edge, graphs):
        for g in graphs:
            if edge in g.edges():
                return True
        return False

    def common_nodes(self,mapping, Original_graphs):
        n_list = []
        for node in mapping.keys():
            for g in Original_graphs:
                if node in g.nodes():
                    n_list.append(node)
                    break
        return set(n_list)
