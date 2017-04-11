import linking_test
from multilayer_test import *
from Node2Vec import *
from Word2Vec import *
import os, time


##################import multiple network#####################

start = time.time()
portion = 0.1
path = sys.argv[1]
mt = MultT(portion, path)
Removelist, tempath = mt.sample_n()
print("Removelist length: ", len(Removelist))

BFSmap, graphs, M_graph = read_dic(tempath)
M_BFSlist, M_Edgelist = read_data(tempath + '/' + M_graph + ".txt")
print("Sampled Merge edge list length: ", len(M_Edgelist))

p = 0.5
q = 0.5
num_walks = 10
walk_length = 80

M_G = Graph(M_BFSlist, M_Edgelist, p, q)
M_G.preprocess_transition_probs()
M_walks = M_G.simulate_walks(num_walks, walk_length)

M_words = []
for walk in M_walks:
	M_words.extend([str(step) for step in walk])

M_L = Learn(M_words)
M_matrix, M_mapping = M_L.train()

BFSlist, Edgelist = read_data(path + '/merged_graph.txt')

M_T = linking_test.Test(BFSlist, Edgelist, portion)
percentage, AUC = M_T.run_test(Removelist, M_matrix, M_mapping, BFSlist)
print("the percetion of prediction is %f "%percentage)
print("the AUC of prediction is %f"%AUC)


T_matrix = {}
T_mapping = {}
for g in graphs:
    G = Graph(BFSmap[g], graphs[g], p, q)
    G.preprocess_transition_probs()
    walks = G.simulate_walks(num_walks, walk_length)
    words = []
    for walk in walks:
	    words.extend([str(step) for step in walk])
    L = Learn(words)
    matrix, mapping = L.train()
    T_matrix[g] = matrix
    T_mapping[g] = mapping
    '''
    if T_matrix == []:
        T_matrix = matrix
    else:
        print("T_matrix dimension", len(T_matrix))
        print("matrix dimension", len(matrix))
        for i in range(len(T_matrix)):
            #print(type(matrix))
            #print(type(matrix[i]))
            print("i:", i)
            T_matrix[i] = np.concatenate((T_matrix[i], matrix[i]))
    '''
#print(T_matrix)
T_percetion, T_AUC = mt.run_test(Removelist, T_matrix, T_mapping, BFSlist, portion)
print("the percetion of prediction is %f "%T_percetion)
print("the AUC of prediction is %f"%T_AUC)
print("Total time comsumed %fs" %(time.time()-start))
