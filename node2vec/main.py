# Sailung Yeung
# <yeungsl@bu.edu>
# reference:
# http://www.cnblogs.com/edwardbi/p/5509699.html

import numpy as np
import networkx as nx
import pickle
import Node2Vec, Word2Vec, linking_test, link_pred, multilayer_test, Node2Vec_MKII, MK_test
import collections, math, os, random, sys, time, argparse

# Read in the same data as used in tensoflow template
# https://github.com/tensorflow/tensorflow/blob/master/tensorflow/examples/tutorials/word2vec/word2vec_basic.py
# for comparasion


################ helper function ###################################
def reader(path):
  files = os.listdir(path)
  nx_graphs = []
  for name in files:
    if name.endswith(".pickle"):
      print(path+name)
      g = pickle.load(open(path + name, "rb"))
      nx_graphs.append(max(nx.connected_component_subgraphs(g), key=len))
  return nx_graphs

################ global parameter ###################################
working_dir = os.getcwd()
filename = ""
path = ""
test_N = False
test_C = False
test_E = False
test_MN = False
test_ME = False
test_MNMK = False
test_MNOF = False
test_all = False
p = 0.5
q = 0.5
num_walks = 10
walk_length = 80
percent = 0.1

################# flag reading #######################################
parser = argparse.ArgumentParser()
parser.add_argument('-g', '--graph', help='input one graph for runing the test')
parser.add_argument('test', help='N for node2vec, C for CommonNeighbors, E for NetEmbedding, MN for Multilayer node2vec, ME for Multilayer NetEmbeding')
parser.add_argument('-d', '--directory', help='a folder that contains all the graphs for multilayer test')

args = parser.parse_args()
if args.test == 'N':
  print('running Node2Vec on ', args.graph)
  test_N = True
  filename = args.graph
elif args.test == 'C':
  print('running CommonNeighbors and Jaccard on', args.graph)
  test_C = True
  filename = args.graph
elif args.test == 'E':
  print('running Network Embedding on', args.graph)
  test_E = True
  filename = args.graph
elif args.test == 'MN' and args.directory != None:
  test_MN = True
  path = args.directory
elif args.test == 'ME' and args.directory != None:
  test_ME = True
  path = args.directory
elif args.test == 'MNMK' and args.directory != None:
  test_MNMK = True
  path = args.directory
elif args.test == 'MNOF' and args.directory != None:
  test_MNOF = True
  path = args.directory
elif args.test == 'all' and args.directory != None:
  test_all =True
  path = args.directory
  filename = args.graph

################# main code ###########################################
start = time.time()
if filename != "":
  #### sampling data
  BFSlist, Edgelist = linking_test.read_data(filename)
  #print("BFSlist: ", BFSlist)

  print('edge list size', len(Edgelist))
  T = linking_test.Test(BFSlist, Edgelist, percent)
  Removelist, New_BFSlist, New_Edgelist = T.sample()
  print('New edge list size', len(New_Edgelist))
  #print('Removelist: ', Removelist)
  #print("New BFSlist", New_BFSlist)
  #print("New Edgelist", New_Edgelist)

if test_all or test_N:

  ##### running Node2Vec

  G = Node2Vec.Graph(New_BFSlist, New_Edgelist, p, q)
  G.preprocess_transition_probs()
  walks = G.simulate_walks(num_walks, walk_length)
  print('walk list size', len(walks))
  words = []
  for walk in walks:
    words.extend([str(step) for step in walk])

  L = Word2Vec.Learn(words)
  matrix, mapping = L.train()
  #print(mapping)
  percentage, AUC = T.run_test(Removelist, matrix, mapping, BFSlist)
  results = open(working_dir + '/' + filename.split(".txt")[0] + "Node2Vec_result.txt", 'w+')
  results.write('AUC' + '\t' + str(AUC) + '\n' + 'P' + '\t' + str(percentage))
  print("the percetion of prediction is %f "%percentage)
  print("the AUC of prediction is %f"%AUC)
  #print("Total time comsumed %fs" %(time.time()-start))
  print('done running Node2Vec !!!!!!!')

if test_all or test_C:

  ###### running CommonNeighbors and Jaccard
  p = link_pred.Prediction()
  vetex_set = p.create_vertex(New_Edgelist)
  matrix_old = p.create_adjmatrix(Edgelist, vetex_set)
  matrix_new = p.create_adjmatrix(New_Edgelist, vetex_set)
  ## doing common Neighbors
  cn = link_pred.CommonNeighbors()
  score_cn = cn.fit(matrix_old)
  auc_cn = p.auc_score(score_cn, matrix_old, matrix_new, 'cc')

  #print(matrix_new)
  #print(matrix_old)
  #print(score_cn)


  ## doing jaccard
  ja = link_pred.Jaccard()
  score_ja = ja.fit(matrix_old)
  auc_ja = p.auc_score(score_ja, matrix_old, matrix_new, 'cc')
  results = open(working_dir + '/' + filename.split(".txt")[0] + "CJ_result.txt", 'w+')
  results.write('Common_AUC' + '\t' + str(auc_cn) + '\n' + 'Jaccard_AUC' + '\t' + str(auc_ja))
  print('common neighbors auc', auc_cn)
  print('jaccard auc', auc_ja)
  print('done running CommonNeighbors and Jaccard!!!!!!!!')

if test_all or test_E:

  ####### generating files needed in Net Embedding
  input_file = filename.split('.txt')[0] + '_sample.txt'
  with open(working_dir + '/' + input_file, 'w+') as f:
    for edge in New_Edgelist:
      f.write(str(edge[0]) + '\t' + str(edge[1]) + '\n')

  ####### starting running Net Embedding
  os.system('python3 generate_facts.py %s' %input_file)
  os.system('./Embedding -network_name %s -generate_flag 0' %input_file)

  mapping_file = working_dir + '/tmp/node_2_id.txt'
  mapping = {}
  with open(mapping_file,'r') as f:
    for line in f.readlines():
      node,id = line.strip().split()
      mapping[node]=int(id)

  matrix_file = working_dir + '/tmp/%s.node' %input_file
  matrix = []
  with open(matrix_file,'r') as f_m:
    for line in f_m.readlines():
      tmp = line.strip().split()
      tmp_float = [float(_) for _ in tmp]
      matrix.append(np.array(tmp_float))

  percentage, AUC = T.run_test(Removelist, matrix, mapping, BFSlist)
  results = open(working_dir + '/' + filename.split(".txt")[0] + "NetEmbeding_result.txt", 'w+')
  results.write('AUC' + '\t' + str(AUC) + '\n' + 'P' + '\t' + str(percentage))
  print(("the percetion of prediction is %f "%percentage))
  print("the AUC of prediction is %f"%AUC)
  print('done running Net Embedding!!!!!!!!')

if test_all or test_MN:
  mt = multilayer_test.MultT(percent, path)
  Removelist, tempath = mt.sample_n()
  print("Removelist length: ", len(Removelist))

  BFSmap, graphs, M_graph = multilayer_test.read_dic(tempath)
  M_BFSlist, M_Edgelist = multilayer_test.read_data(tempath + '/' + M_graph + ".txt")
  print("Sampled Merge edge list length: ", len(M_Edgelist))

  M_G = Node2Vec.Graph(M_BFSlist, M_Edgelist, p, q)
  M_G.preprocess_transition_probs()
  M_walks = M_G.simulate_walks(num_walks, walk_length)

  M_words = []
  for walk in M_walks:
    M_words.extend([str(step) for step in walk])

  M_L = Word2Vec.Learn(M_words)
  M_matrix, M_mapping = M_L.train()

  BFSlist, Edgelist = multilayer_test.read_data(path + '/merged_graph.txt')

  M_T = linking_test.Test(BFSlist, Edgelist, percent)
  percentage, AUC = M_T.run_test(Removelist, M_matrix, M_mapping, BFSlist)
  results = open(working_dir + '/' + filename.split(".txt")[0] + "Multilayer_Node2vec_result.txt", 'w+')
  results.write('Combined_AUC' + '\t' + str(AUC) + '\n' + 'Combined_P' + '\t' + str(percentage)+ '\n')
  print("the percetion of prediction is %f "%percentage)
  print("the AUC of prediction is %f"%AUC)


  T_matrix = {}
  T_mapping = {}
  for g in graphs:
    G = Node2Vec.Graph(BFSmap[g], graphs[g], p, q)
    G.preprocess_transition_probs()
    walks = G.simulate_walks(num_walks, walk_length)
    words = []
    for walk in walks:
      words.extend([str(step) for step in walk])

    L = Word2Vec.Learn(words)
    matrix, mapping = L.train()
    T_matrix[g] = matrix
    T_mapping[g] = mapping

  #print(T_matrix)
  T_percetion, T_AUC = mt.run_test(Removelist, T_matrix, T_mapping, BFSlist, percent)
  results.write('Seperated_AUC' + '\t' + str(T_AUC) + '\n' + 'Seperated_P' + '\t' + str(T_percetion))
  print("the percetion of prediction is %f "%T_percetion)
  print("the AUC of prediction is %f"%T_AUC)
  print('done running Multilayer Node2Vec')

if test_all or test_ME:
  mt = multilayer_test.MultT(percent, path)
  Removelist, tempath = mt.sample_n()
  print("Removelist length: ", len(Removelist))

  BFSmap, graphs, M_graph = multilayer_test.read_dic(tempath)
  M_BFSlist, M_Edgelist = multilayer_test.read_data(tempath + '/' + M_graph + ".txt")
  print("Sampled Merge edge list length: ", len(M_Edgelist))

  ######## generating files needed in Net Embedding
  input_file = 'merged_sample.txt'
  with open(working_dir + '/' + input_file, 'w+') as f:
    for edge in M_Edgelist:
      f.write(str(edge[0]) + '\t' + str(edge[1]) + '\n')

  ####### starting running Net Embedding
  os.system('python3 generate_facts.py %s' %input_file)
  os.system('./Embedding -network_name %s -generate_flag 0' %input_file)

  mapping_file = working_dir + '/tmp/node_2_id.txt'
  mapping = {}
  with open(mapping_file,'r') as f:
    for line in f.readlines():
      node,id = line.strip().split()
      mapping[node]=int(id)

  matrix_file = working_dir + '/tmp/%s.node' %input_file
  matrix = []
  with open(matrix_file,'r') as f_m:
    for line in f_m.readlines():
      tmp = line.strip().split()
      tmp_float = [float(_) for _ in tmp]
      matrix.append(np.array(tmp_float))

  BFSlist, Edgelist = multilayer_test.read_data(path + '/merged_graph.txt')

  M_T = linking_test.Test(BFSlist, Edgelist, percent)
  percentage, AUC = M_T.run_test(Removelist, matrix, mapping, BFSlist)
  results = open(working_dir + '/' + filename.split(".txt")[0] + "NetEmbeding_result.txt", 'w+')
  results.write('merged_AUC' + '\t' + str(AUC) + '\n' + 'merged_P' + '\t' + str(percentage) + '\n')
  print(("the percetion of prediction is %f "%percentage))
  print("the AUC of prediction is %f"%AUC)

  T_matrix = {}
  T_mapping = {}
  for g in graphs:
    input_s = g + '_sample.txt'
    with open(working_dir + '/' + input_s, 'w+') as f:
      for edge in graphs[g]:
        f.write(str(edge[0]) + '\t' + str(edge[1]) + '\n')
    os.system('python3 generate_facts.py %s' %input_s)
    os.system('./Embedding -network_name %s -generate_flag 0' %input_s)

    mapping_file_s = working_dir + '/tmp/node_2_id.txt'
    mapping_s = {}
    with open(mapping_file_s,'r') as f:
      for line in f.readlines():
        node,id = line.strip().split()
        mapping_s[node]=int(id)

    matrix_file_s = working_dir + '/tmp/%s.node' %input_s
    matrix_s = []
    with open(matrix_file_s,'r') as f_m:
      for line in f_m.readlines():
        tmp = line.strip().split()
        tmp_float = [float(_) for _ in tmp]
        matrix_s.append(np.array(tmp_float))

    T_matrix[g] = matrix_s
    T_mapping[g] = mapping_s
  #print(T_matrix)
  T_percetion, T_AUC = mt.run_test(Removelist, T_matrix, T_mapping, BFSlist, percent)
  results.write('separated_AUC' + '\t' + str(T_AUC) + '\n' + 'separated_P' + '\t' + str(T_percetion))
  print("the percetion of prediction is %f "%T_percetion)
  print("the AUC of prediction is %f"%T_AUC)
  print("network embedding multilayer test done!!!!")

if test_all or test_MNMK:
  files = os.listdir(path)
  nx_graphs = []
  for name in files:
    if name.endswith(".pickle"):
      print(path+name)
      g = pickle.load(open(path + name, "rb"))
      nx_graphs.append(max(nx.connected_component_subgraphs(g), key=len))

  MK_T = MK_test.Test(path, percent)
  MK_T.readG()
  graphs = MK_T.sample()

  MK_G = Node2Vec_MKII.Graph(graphs, p, q)
  MK_G.preprocess_transition_probs()
  MK_walks = MK_G.simulate_walks(num_walks, walk_length)

  MK_words = []
  for walk in MK_walks:
    MK_words.extend([str(step) for step in walk])


  M_L = Word2Vec.Learn(MK_words)
  M_matrix, M_mapping = M_L.train()

  percetion, AUC = MK_T.run_test(M_matrix, M_mapping, nx_graphs)
  print("the percetion of prediction is %f "%percetion)
  print("the AUC of prediction is %f"%AUC)
  print("node2vec MKII link prediction sampling test done!!!!")

if test_all or test_MNOF:
  online_dir = path+"online/"
  online_graphs = reader(online_dir)
  offline_dir = path+"offline/"
  offline_graphs = reader(offline_dir)

  off_G = Node2Vec_MKII.Graph(offline_graphs, p, q)
  off_G.preprocess_transition_probs()
  off_walks = off_G.simulate_walks(num_walks, walk_length)

  off_words = []
  for walk in off_walks:
    off_words.extend([str(step) for step in walk])


  off_L = Word2Vec.Learn(off_words)
  off_matrix, off_mapping = off_L.train()

  on_G = Node2Vec_MKII.Graph(online_graphs, p, q)
  on_G.preprocess_transition_probs()
  on_walks = on_G.simulate_walks(num_walks, walk_length)

  on_words = []
  for walk in on_walks:
    on_words.extend([str(step) for step in walk])


  on_L = Word2Vec.Learn(on_words)
  on_matrix, on_mapping = on_L.train()

  MK_T = MK_test.Test(path, percent)
  off_percetion, off_AUC = MK_T.run_matching_test(off_matrix, off_mapping, online_graphs)
  on_percetion, on_AUC = MK_T.run_matching_test(on_matrix, on_mapping, offline_graphs)
  print("Using offline group to match online group....")
  print("percetion: %f, AUC: %f"%(off_percetion, off_AUC))
  print("Using online group to match offline group.....")
  print("percetion: %f, AUC: %f"%(on_percetion, on_AUC))
  print("node2vec MKII link prediction on-off line test done!!!!")
