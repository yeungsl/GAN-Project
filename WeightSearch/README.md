# Weight Search Algorithm and Simulator of the network
This directory contains two classes the implementation of weight search algorithm and the simulator.
The toolchain has to support C++11.
## Build
To build the executable in main.cc into test

```
g++ main.cc llsq.cpp WeightSearch.cc simulator.cc -o test
```
I recommend build under C++11

## Running the tests
The executable takes one input file, which should be a list of edges (a pair of int).
```
./test <filename>
```
The output will be a simulation result with the number of edges selected by the algorithm and running time in each round of simulation.

### example
```
./test 2004-04.txt
```
