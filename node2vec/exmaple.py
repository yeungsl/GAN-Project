import link_pred
import linking_test

# Read the data into a list of strings.
def read_data(filename):
  """Extract the file and convert it into a neighbor list"""
  BFSlist = {}
  Edgelist = []
  for line in open(filename):
    s, d = line.split(" ")
    src = s
    dst = d
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





filename = sys.argv[1]
BFSlist, Edgelist = read_data(filename)
print('edge list size', len(Edgelist))
T = linking_test.Test(BFSlist, Edgelist, float(sys.argv[2]))
Removelist, New_BFSlist, New_Edgelist = T.sample()
print('New edge list size', len(New_Edgelist))

p = Prediction()
vetex_set = p.create_vertex(New_Edgelist)
matrix_old = p.create_adjmatrix(Edgelist, vetex_set)
matrix_new = p.create_adjmatrix(New_Edgelist, vetex_set)

cn = CommonNeighbors()

score_cn = cn.fit(matrix_old)
auc_cn = p.auc_score(score, matrix_old, matrix_new, 'cc')

print(matrix_new)
print(matrix_old)
print(score)
print('auc', auc_cn)

