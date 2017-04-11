import os, sys, random, itertools, collections
import numpy as np

def read_data(filename):
    """Extract the file and convert it into a neighbor list"""

    BFSlist = {}
    Edgelist = []
    for line in open(filename):
        (s, d) = line.split('\t')
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

def read_dic(path):
        files = os.listdir(path)
        M_graph = ''
        graphs = dict()
        BFSmap = dict()
        for name in files:
                if name.endswith(".txt"):
                        if "merged_graph" in name:
                                M_graph = name.split(".txt")[0]
                        else:
                                BFSlist , edgelist =  read_data(path + '/' + name)
                                graphs[name.split(".txt")[0]] = edgelist
                                BFSmap[name.split(".txt")[0]] = BFSlist
                                print("file: %s has %i edges" %(name, len(edgelist)))
        if M_graph == '':
                sys.exit("cannot find the merged graph in the directory!!")
        return (BFSmap, graphs, M_graph)



class MultT:
        def __init__(self, p, path):
                self.P = p
                self.Path = path

        def sample_n(self):
                p = self.P
                path = self.Path
                _, graphs, M_graph = read_dic(path)
                M_BFSlist, M_Edgelist = read_data(path + '/' + M_graph + ".txt")
                #print(M_Edgelist)
                print ("Merged edge list length:", len(M_Edgelist))
                if not os.path.exists(path + '/tmp'):
                        os.mkdir(path +'/tmp')
                samplefile = open(path + '/tmp/' + M_graph + "_sample.txt", "w+")
                Removelist = []
                for edge in M_Edgelist:
                        r = random.random()
                        if r < p:
                                if len(M_BFSlist[edge[0]]) == 1 or len(M_BFSlist[edge[1]]) == 1:
                                        samplefile.write(str(edge[0]) + '\t' + str(edge[1]) + '\n')
                                        continue
                                Removelist.append(edge)
                        else:
                                samplefile.write(str(edge[0]) + '\t' + str(edge[1]) + '\n')

                samplefile.close()

                for edge in Removelist:
                        for g in  graphs:
                                if edge in graphs[g]:
                                        graphs[g].remove(edge)
                                        break
                for g in graphs:
                        with open(path + '/tmp/' + g + "_sample.txt" , "w+") as f:
                                f.writelines([str(edge[0]) + '\t' + str(edge[1]) + '\n' for edge in graphs[g]])
                                f.close()
                return (Removelist, path + '/tmp')
        def check(self, src, dst):
                mapping = self.MP
                matrix = self.M
                path = self.Path
                s_ind = -1
                s_g = -1
                d_ind = -1
                d_g = -1
                for g in mapping:
                        if src in mapping[g].keys():
                                s_ind = mapping[g][src]
                                s_g = g
                                if dst in mapping[g].keys():
                                        d_ind = mapping[g][dst]
                                        d_g = g
                        elif dst in mapping[g].keys():
                                d_ind = mapping[g][dst]
                                d_g = g
                        if s_ind != -1 and d_ind != -1:
                                break
                if s_ind == -1 or d_ind == -1:
                        with open(path + '/tmp/error.txt', 'w+') as f:
                                f.write("src: %s, dst: %s" %(src, dst))
                                f.write(mapping)
                        sys.exit("cannot find index in the mappings")

                r = np.linalg.norm(matrix[s_g][s_ind] - matrix[d_g][d_ind])
                return r

        def run_test(self, Removelist, matrix, mapping, Original_list, perportion):
                self.M = matrix
                self.MP = mapping
                p = perportion
                result = {}
                s = 0
                node_list = set([node for edge in Removelist for node in edge])
                for edge in itertools.combinations(node_list, 2):
                        dist = self.check(edge[0], edge[1])
                        s += dist
                        result[edge] = dist

                normalized_result = {}
                for e in result:
                        normalized_result[e] = result[e] / s

                sorted_result = collections.OrderedDict(sorted(normalized_result.items(),key=lambda t: t[1]))

                n = len(normalized_result) * p
                correct = 0
                count = 1
                print ('getting the first ', n)

                for edge in sorted_result:

                        if edge[1] in Original_list[edge[0]].keys() or edge[0] in Original_list[edge[0]].keys():
                                correct += 1
                        count += 1
                        if count > n:
                                break
                print ('correct', correct)

                AUC = (correct * 0.5 + n - correct) / n
                return (correct / n, AUC)
