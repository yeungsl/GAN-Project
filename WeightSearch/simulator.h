/**
 * purpose : implement the Weight Search Algorithm
 * @file simulator.h
 * @brief implement a simulator
 * Details.
 * 1. implement a simulator
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
class simulator{
 private:
  std::vector<std::pair<int, int>> edge_list_;
  std::vector<std::pair<int, int>> selected_edges;
  void randomValue(std::pair<int, int>edge);
 public:
  std::map<std::pair<int, int>, double> W_t_;
  void setParam(std::vector<std::pair<int, int>> list);
  void generateNext(double p);
  void printWt();
};

