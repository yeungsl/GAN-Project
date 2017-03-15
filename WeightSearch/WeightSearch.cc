/**
 * purpose : implementation of WeightSearh.h
 * @file WeightSearch.cc
 * @brief  implementation of WeightSearh.h
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
#include "WeightSearch.h"


void weightSearch::initializeLists(std::vector<std::pair<int, int>> edge_list){
  for (auto edge: edge_list){
    D_w[edge].push_back(init_value);
    D_shake[edge] = 0;
  }
}

void weightSearch::setParam(double init_value_, std::vector<std::pair<int, int>> edge_list){
  init_value = init_value_;
  initializeLists(edge_list);
}


void weightSearch::printDw(){
  std::cout<< "D_w has length:" << D_w.size()<<std::endl;
  for (auto edge:D_w){
    std::cout<< "(" << edge.first.first << "," << edge.first.second <<") :";
    for (auto weight: edge.second){
      std::cout<< weight <<",";
    }
    std::cout<< std::endl;
  }
}

void weightSearch::printDshake(){
  std::cout<< "D_shake has length:" << D_shake.size()<<std::endl;
  for (auto edge:D_shake){
    std::cout<< "(" << edge.first.first << "," << edge.first.second <<")"
	     << ":" << edge.second << std::endl;
  }
}

std::vector<std::pair<int, int>> weightSearch::search( std::map<std::pair<int, int>, double> W_t,
						       double jump, int N_shake, int L){

  // easy structure for search but too complicated for simulation std::map<int, std::vector<std::map<int,double>>> edge_list;
  // Initialize edge_list = [];
  std::vector<std::pair<int, int>> edge_list;
  // For each edge in W_t
  for (auto element : W_t){
    // Calculate change of weight

    auto src_dst = element.first;
    auto Weight_now = element.second;
    auto Weight_list = D_w[src_dst];
    auto Weight_zero = Weight_list[0];
    auto delta_weight = fabs(fabs(Weight_now - Weight_zero) - Weight_list[Weight_list.size()-1]);
    
    // If delta_weight is larger than jump and not a shake
    if (delta_weight >= jump && D_shake[src_dst] < N_shake){
      // Insert edge in the edge_list
      edge_list.push_back(src_dst);
      // Delete edge from D_w;
      D_w.erase(src_dst);
      // Restore the initail state of edge
      D_w[src_dst].push_back(init_value);
      // Increament the jump counter in D_shake
      D_shake[src_dst]++;
    }else if(delta_weight != 0){
      // Calculate change of weight relative to t_0
      auto delta_weight_zero = fabs(Weight_now - Weight_zero);
      // Insert change of weight relative to t_0 into D_w
      D_w[src_dst].push_back(delta_weight_zero);
      if (D_w[src_dst].size() >= L){
	// Calculate trend for edge

	int n = D_w[src_dst].size();
	double k;
	double b;
	double x[n];
	double y[n];
	// Filling in variable x and variable y
	for (int i = 0; i < n; i++){
	  x[i] = i;
	  y[i] = D_w[src_dst][i];
	}
	// Then put into the llsq function to get the relationship
	// The llsq function is from:
	// https://people.sc.fsu.edu/~jburkardt/cpp_src/llsq/llsq.html
	llsq(n, x, y, k, b);
	if (k > 0){
	  // Insert edge into the edge_list
	  edge_list.push_back(src_dst);
	  // Delete edge from D_w
	  D_w.erase(src_dst);
	  // Restore the state of the edge
	  D_w[src_dst].push_back(init_value);
	}
      }
    }
  }
  return edge_list;
}





