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
#include <vector>
#include <set>
#include <map>
#include <string>
#include <cmath>
#include "llsq.hpp"


/**
 * @brief Assumption: edge -- std::pair<int, int> a pair of src node and dst node
 *                    weight -- double a value on certain edge range from [0, 1]
 * @author yeungsl@bu.edu
 * @date 2017.03.11
 * 
 * @param Input:
 *        D_w -- a map of edge to a list of delta weight, which is a vector of double
 *        D_shake -- a map of edge to number of jumps it made, which is just an int
 *        W_t -- a map of edge to its weight, whihc is a double
 *        delta_jump -- the number for the case that  once the delta weight exceed will be count as a jump
 *        N_shake -- the number for the case that once the count exceed will be count as shake
 *        L -- the number for the case that once the length of D_w for one edge exceeds will check if it is long-term shake
 *
 * @param Output:
 *        edgelist -- a list of eadges who has the changes that worth noticing (either a jump, shake, or a long-term shake)
 * 
 */


class weightSearch{
 private:
  std::map<std::pair<int, int>, std::vector<double>> D_w;
  std::map<std::pair<int, int>, int> D_shake;
  double init_value = 0.0;
  void initializeLists(std::vector<std::pair<int, int>> edge_list);
 public:
  std::vector<std::pair<int, int>> search(std::map<std::pair<int, int>, double> W_t,
					  double delta_jump, int N_shake, int L);
  void setParam( double init_value_, std::vector<std::pair<int, int>> edge_list);
  void printDw();
  void printDshake();

/*
void weightSearch(std::map<int, std::vector<std::map<int,std::vector<double>>>> D_w, 
		  std::map<int, std::vector<std::map<int,int>>> D_shake,
		  std::map<int, std::vector<std::map<int,double>>>W_t, double delta_jump, int N_shake, int L){

*/

};
