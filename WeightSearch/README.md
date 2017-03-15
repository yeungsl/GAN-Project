# Weight Search Algorithm and Simulator of the network
This directory contains two classes the implementation of weight search algorithm and the simulator.
The toolchain has to support C++11.
## Build
To build the executable in main.cc into test

```
make
```

To build again after fixing some files, run make clean first, then run make
```
make clean
make
```

## Running the tests
The executable takes one file for input network one file for output the edge that searched in the algorithm.
```
./runSim <filename1> <filename2>
```
The output will be a simulation result with the number of edges selected by the algorithm and running time in each round of simulation.

### example
```
./runSim 2004-04.txt out.txt
```
