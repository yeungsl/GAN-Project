#@author Sailung Yeung <yeungsl@bu.edu>
#@reference: https://github.com/xinbingzhe/LinkPrediction

import numpy as np
import random
import pandas as pd
import numpy.matlib


class Prediciton():
	def create_vertex(nodepair_set):
    '''
            nodepair_set : [[i,j],[i,k],......]
            return:vertex_set {i:0,j:1,k:2,...}
    '''
    # 产生vertex id 对应的字典 为了保证所有邻接矩阵所对应的的位置都一样
    vertex_set = {}
    num = 0
    for i in nodepair_set:
        if i[0] not in vertex_set:
            vertex_set[i[0]] = num
            num += 1
        if i[1] not in vertex_set:
            vertex_set[i[1]] = num
            num += 1
    return vertex_set

    def create_adjmatrix(nodepair_set,vertex_set):
    '''
                nodepair_set  [ [i,j],[p,q],....]
                根据不同的顶点对，产生不同邻接矩阵
    '''
    init_matrix = np.zeros([len(vertex_set),len(vertex_set)])

    for pair in nodepair_set:
        if pair[0] in vertex_set and pair[1] in vertex_set:
            init_matrix[  vertex_set[pair[0]] ] [ vertex_set[pair[1]] ] = 1 
            init_matrix[  vertex_set[pair[1]] ] [ vertex_set[pair[0]] ] = 1 
    return init_matrix

    def auc_score(matrix_score,matrix_test,matrix_train,n_compare=10):
    '''
            根据测试顶点的邻接矩阵，分出发生链接与没有发生链接的集合
            n_compare: int,'cc' ，计算auc比较次数，当该参数输入为int型时为比较次数，当输入为cc时以为Complete comparison，完全比较，默认参数为10
    '''
    import numpy as np
    import random

    if type(n_compare) == int:
        if len(matrix_test[0]) < 2:
            raise Exception("Invalid ndim!", train.ndim)
        elif len(matrix_test[0]) < 10:
            n_compare = len(matrix_test[0])
    else:
        if n_compare != 'cc':
            raise Exception("Invalid n_compare!", n_compare)

    unlinked_pair = []
    linked_pair = []

    #print(matrix_score[0][0])

    l = 1
    for i in range(0,len(matrix_test)):
        for j in range(0,l):
            if i != j and matrix_train[i][j]!=1: # 去掉训练集中已经存在的边
                if matrix_test[i][j] == 1:
                    linked_pair.append(matrix_score[i,j])
                elif matrix_test[i][j] == 0:
                    unlinked_pair.append(matrix_score[i,j])
                else:
                    raise Exception("Invalid connection!", matrix_test[i][j])
        l += 1

    auc = 0.0
    if n_compare == 'cc':
        frequency = min(len(unlinked_pair),len(linked_pair))
    else:
        frequency = n_compare
    for fre in range(0,frequency):
        unlinked_score = float(unlinked_pair[random.randint(0,frequency-1)])
        linked_score = float(linked_pair[random.randint(0,frequency-1)])
        if linked_score > unlinked_score:
            auc += 1.0
        elif linked_score == unlinked_score:
            auc += 0.5
    
    auc = auc/frequency
    
    return auc

class  similarity(object):
    """docstring for  similarity"""
    
    def fit(self,train_adj):
        "矩阵维度大于1"
        train = np.matrix(train_adj)
        if train.ndim < 2:
            raise Exception("Invalid ndim!", train.ndim)
        if train.size < 2:
            raise Exception("Invalid size!", train.size)
        if train.shape[0] != train.shape[1]:
            raise Exception("Invalid shape!", train.shape)


class CommonNeighbors(similarity):
    """
            CommonNeighbors 求交集
    """
    def fit(self,train_adj):
        similarity.fit(self,train_adj)
        train_adj = np.matrix(train_adj)

        return train_adj * train_adj

class Jaccard(similarity):
    """
            两顶点邻居的交集与并集之比
    """
    def fit(self,train_adj):
        similarity.fit(self,train_adj)
        train_adj = np.matrix(train_adj)
        numerator =  train_adj * train_adj
        deg0 = np.matlib.repmat(train_adj.sum(0),len(train_adj),1)
        deg1 = np.matlib.repmat(train_adj.sum(1),1,len(train_adj))
        denominator = deg0 + deg1 - numerator
        sim = numerator/denominator
        sim[np.isnan(sim)] = 0
        sim[np.isinf(sim)] = 0
        return sim