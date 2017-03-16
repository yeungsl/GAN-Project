/**
 * purpose : implement the Weight Search Algorithm
 * @file WeightSearch.h
 * @brief implement the Weight Search Algorithm
 * Details.
 * 1. implement the Weight Search Algorithm
 *
 * @author Sailung Yeung
 * @email yeungsl@bu.edu
 * @version 1.0.0.0
 * @date 2017.03.11
 *----------------------------------------------------------------------------*
 *  Change History :                                                          *
 *  <Date>     | <Version> | <Author>       | <Description>                   *
 *----------------------------------------------------------------------------*
 *  2017/03/11 | 1.0.0.0   | Sailung Yeung  | Create file                     *
 *----------------------------------------------------------------------------*
 * */

#include <iostream>
#include <fstream>
#include <vector>
#include <set>
#include <map>
#include <cmath>
#include <string>
#include <random>
#include <chrono>
#include "simulator.h"
#include "weightSearch.h"

std::vector<std::pair<int, int>> readFileToEdgeList(std::string filename);
void displayEdgeList(std::vector<std::pair<int, int>> v);

std::vector<std::pair<int, int>> readFileToEdgeList(const std::string filename){
  std::ifstream source;
  source.open(filename);
  std::vector<std::pair<int, int>> edge_list;
  std::string line;
  while (std::getline(source, line)){
    std::string deliminate = " ";
    auto src = std::stoi(line.substr(0, line.find(deliminate)));
    auto dst = std::stoi(line.substr(line.find(deliminate)));
    auto edge = std::make_pair (src, dst);
    edge_list.push_back(edge);
  }
  return edge_list;
}

void displayEdgeList(std::vector<std::pair<int, int>> v){
  for (int i(0); i != v.size(); ++i){
    std::cout << "("<< v[i].first << "," << v[i].second << ")" << "\n";
  }
}

int main(int argc,  char *argv[]){
  std::vector<std::pair<int, int>> edges;
  if (argc > 2 ){
    std::string filename(argv[1]);
    std::cout<< "Input network: "<< filename << std::endl;
    edges = readFileToEdgeList(filename);
    //displayEdgeList(edges);
  }else{
    std::cout<< "Have to input a network file and a output file" << std::endl;
    return 1;
  }
  std::set<std::pair<int, int>> output;
  
  simulator s;
  weightSearch w;
  double jump = 0.5;
  int N_shake = 3;
  int L = 1000;
  int init_value = 0.0;
  double p = 0.2;
  int simulation_round = 5;
  std::cout<< "Got edges input :" << edges.size() << std::endl;
  w.setParam(init_value, edges);
  s.setParam(edges);

  std::chrono::duration<double> time_sum;
  for(int i(0); i < simulation_round; i++){
    // auto start = std::chrono::system_clock::now();
    s.generateNext(p);
    //s.printWt();
    auto start = std::chrono::system_clock::now();
    auto r_edges = w.search(s.W_t_, jump, N_shake, L);
    auto end = std::chrono::system_clock::now();
    time_sum += (end - start);
    for(auto edge: r_edges){
      output.insert(edge);
    }
    //w.printDw();
    //displayEdgeList(r_edges);    
    //auto end = std::chrono::system_clock::now();
    //std::chrono::duration<double> time_sec = end - start;
    //std::cout<< "edges worth attention: " << r_edges.size() << std::endl;
    //std::cout<< "duration for each round: " << time_sec.count() << std::endl;
  }

  std::cout<< "general time spend:" << time_sum.count()<< "s" << "\n"
	   << "average time spend on each loop: " << time_sum.count()/(double) simulation_round << "s" <<std::endl;
  
  // Writing the output into the file
  std::string outputfile(argv[2]);
  std::cout<< "Output network:" << outputfile<< std::endl;
  std::ofstream o;
  o.open(outputfile);
  for(std::set<std::pair<int, int>>::iterator it = output.begin(); it != output.end(); ++it){
      o << it->first << " " << it->second << "\n";
    }
  o.close();
}

