# Node2Vec
This directory is an implementation of node2vec algorithm with tensorflow by defualt the main script will run random walk and do a learn then test with linking classification.
## Build
Need tensorflow library in python 3
## Running the modele
Run the test with the main.py with a edge list, an output file, and a flag to decide whether to run the second test.
```
python main.py <edgelist.txt> <output.txt> <int>
```
### Input
The input of the python script should be a list of edge 2004-04.txt should be an example
#### running the test without second test
```
python main.py 2004-04.txt out.txt 0
```
#### running the test with the second test
```
python main.py 2004-04.txt out.txt 1
```
### Output
The output of the python script should be an dictionary that contains the test result:
A list of edges sampled with their distances in the matrix.
