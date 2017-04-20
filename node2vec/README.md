# Node2Vec
This directory is an implementation of node2vec algorithm with tensorflow by defualt the main script will run random walk and do a learn then test with linking classification.
## Build
Need tensorflow library in python 3
## Running the modele
Run the test with the main.py with a edge list, an output file, and a flag to decide whether to run the second test.
```
python main.py <-g Graph> <-d directory> <test>
```
### Input
The input of the python script should be a list of edge 2004-04.txt and a test type or a directory and a multilayer test
#### running the normal test with one graph
```
python main.py -g 2004-04.txt N
```
#### running the multilayer test with a directory of graph __must have the merged graph include into the directory__
```
python main.py -d /a MN
```
### Output
The output of the python script should be an dictionary that contains the test result:
The AUC and the percetion of the tests.
