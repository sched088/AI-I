# Program Overview

Agent chooses the action which leads to the highest utility, which in this case is measured in number of discs the acting agent has on the board. 
Program uses Minimax search with Alpha-Beta pruning (depth limited to 4 in the interest of keeping AI decision time relatively low) to determine 
the move which will lead to the highest utility assuming the opponent is a rational, optimal player.
