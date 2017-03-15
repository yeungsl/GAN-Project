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

#include "simulator.h"

void simulator::setParam(std::vector<std::pair<int, int>> list){
  edge_list_ = list;
  selected_edges.clear();
}


void simulator::generateNext(double p){
  W_t_.clear();
  if (p <= 0  && p >= 1){
    std::cout<< "input should from 0 to 1" << std::endl;
    return;
  }
  std::random_device rd;
  std::mt19937 gen(rd());
  std::uniform_real_distribution<> decission(0,1);
  for (auto edge:edge_list_){
    auto r = decission(gen);
    //std::cout<< r << std::endl;
    auto it = std::find(selected_edges.begin(), selected_edges.end(), edge);
    if(it != selected_edges.end()){
      if (r < 0.5){
	randomValue(edge);
      }else{
	selected_edges.erase(it);
      }
    }else{
      if(r < p){
	randomValue(edge);
	selected_edges.push_back(edge);
      }
    }
  }
  std::cout<< "W_t_ size generated is :" << W_t_.size()<<std::endl;
  //std::cout<< "selected_edges size is :" << selected_edges.size()<<std::endl;
  //printlist(1);
}

void simulator::randomValue(std::pair<int, int>edge){
  std::random_device rd;
  std::mt19937 gen(rd());
  std::uniform_real_distribution<> value(-1, 1);
  auto v = value(gen);
  //std::cout<< "(" << edge.first << "," << edge.second << ")"
  //	   << v << std::endl;
  W_t_[edge] = v;
  return;
}

void simulator::printWt(){
  std::cout<< "W_t has length:" << W_t_.size()<< std::endl;
  for (auto edge:W_t_){
    std::cout<< "(" << edge.first.first << "," << edge.first.second <<")"
	     << ":" << edge.second << std::endl;
  }
}





