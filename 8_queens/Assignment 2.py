# two classes: board and queens

import random
import sys
import copy
import math

""" Change these parameters to customize runs and run counts """
n = 8 ## This is the nxn dimension of the board
run_count = 5000 ## This is the number of iterations to run, each iteration creates a custom board to solve

iterations = 3000 ## This impacts FIRST CHOICE and ANNEALING only. Num of loops before breaking out

anneal_rate = 0.99 ## Impacts 'cooling' rate for Annealing
temp = 100 ## Impacts starting temp or 'randomness' for Annealing.

""" Only one of these should be true. Changes which algorithm to run """
steepest_ascent = False
first_choice = False
anneal = True
""" ---------------------End Parameters----------------------"""


class GenerateBoard:
    """Sets up a random board to start the hill climbs on."""
    """Intuition included are that each queen needs to be on her own column"""
    """Default to size = 8"""

    def __init__(self, start_board=[], size=n):
        self.size = n
        self.start_board = start_board

        if not self.start_board:
            for i in range(n):
                # print("Range iter: " + str(i))
                self.start_board.append(random.randint(0, size - 1))
            print("Starting Board: " + str(start_board))
            print("Board Width: " + str(len(start_board)))
        else:
            print("Board already generated")

    def starting_board(self):
        board_size = len(self.start_board)
        return self.start_board, board_size


class Action:
    """identifies actions that are able to be taken based on current board"""

    def __init__(self, run_count=run_count):
        self.run_count = run_count
        self.run_steps = 0
        self.solve_count = 0
        self.solve_step_count = 0
        for i in range(0, run_count):
            print("Run number: " + str(i))
            self.main_board = GenerateBoard(start_board=[]).start_board
            self.cost = self.total_cost(self.main_board)
            self.solution() #pass in main_board?
        self.analysis()

    def total_cost(self, current_game):  # get cost of current board
        cost = 0
        # board = GenerateBoard()
        # print("Currrent Game: " + str(current_game) + " " + str(n)) #how do I pass in board.size here without generating a board within this function?
        for column in range(n):
            # print("iteration: " + str(column))
            for other_column in range(column + 1, n):
                if current_game[column] == current_game[other_column]:
                            # I don't fully understand current_game.start_board how it references the Class  /// Need to save output from Class to be able to use it in another class. // treating like class but already taken from the class?
                            # This references the class for the starting board,             //check type on a number of things.  // can add break statements
                                # but I also need to use total_cost to iterate through changing board states.
                                # I think that hillclimb_sa properly references new board, but .start_board seems wrong
                    cost += 1

                diag = other_column - column
                # print("Start_board_column: " + str(current_game[0]))
                if current_game[column] == current_game[other_column] - diag:
                    cost += 1
                if current_game[column] == current_game[other_column] + diag:
                    cost += 1
        # print("Cost: " + str(cost))
        return cost

    def solution(self):
        conflicts = 0
        while conflicts != self.cost:
            conflicts = self.cost
            if steepest_ascent == True:
                self.run_steps += 1
                self.hillclimb_sa()
            if first_choice == True:
                self.run_steps += 1
                self.hillclimb_fc()
        if anneal == True:
            self.sim_anneal()
        if self.cost > 0:
            print(self.cost)
            print("no solution found")
        else:
            print(self.cost)
            if not anneal: self.run_steps += 1
            self.solve_count += 1
            self.solve_step_count += self.run_steps
        return self.cost

    def hillclimb_sa(self):
         """We are looking for the steepest ascent move:
         first iterate through board and make sure that we aren't evaluation current queen location (cost = total_cost)
         then move queen to a new row"""

         #####
         # Need to program iterating through the below code until we identify the best local cost minimum
         #
         # Pseudo-code: While loops and break when best_cost = total_cost
         #####

         #look for sa move
         lowest_cost = self.total_cost(self.main_board)
         best_board = self.main_board
         iters = 0
         # print("------Lowest Cost: " + str(lowest_cost))
         # print(best_board)
         for column_queen in range(n):  # Why can I not use current_game.size in place of n?
             # print("Column Queen: " + str(column_queen))
             for check_row_queen in range(n):  # Why can I not use current_game.size in place of n?
                 # print("Row Queen" + str(check_row_queen))
                 # print(self.main_board[column_queen] == check_row_queen)
                 if best_board[column_queen] == check_row_queen: #checking if Queen in this location
                     # reminder: board format [A, B, C, D, E, ..., Z] where the int of each item is the row
                     for column in range(n):
                         for check_row in range(n):
                             if best_board[column] != check_row:
                                test_board = copy.deepcopy(best_board)
                                # new_queen = 0
                                test_board[column] = check_row
                                test_cost = self.total_cost(test_board)
                                # print("Test Cost: " + str(test_cost))
                                if test_cost < lowest_cost:
                                    lowest_cost = test_cost
                                    best_board = test_board
                                    # self.run_steps += 1
                                    # print("Pick Cost True")
         self.main_board = best_board
         self.cost = lowest_cost

    def hillclimb_fc(self):
        ''' first choice hill-climb. Instead of taking "best" solution randomly identify a "better" solution'''
        lowest_cost = self.total_cost(self.main_board)
        best_board = self.main_board
        loop = True
        iters = 0
        while loop == True:
            # print("Loop")
            random_column = random.randint(0, n-1)
            random_queen_loc = best_board[random_column]
            random_new_loc = random.randint(0, n-1)

            if random_new_loc != random_queen_loc:
                test_board = copy.deepcopy(best_board)
                test_board[random_column] = random_new_loc
                test_cost = self.total_cost(test_board)
                # print("Test Cost: " + str(test_cost))
                # print("Lowest Cost: " + str(lowest_cost))
                if test_cost < lowest_cost:
                    lowest_cost = test_cost
                    best_board = test_board
                    loop = False
                    # self.run_steps += 1
            iters += 1
            if iters > iterations:
                break
        self.main_board = best_board
        self.cost = lowest_cost


    def sim_anneal(self, anneal_rate = anneal_rate, temp = temp):
        lowest_cost = self.total_cost(self.main_board)
        best_board = self.main_board
        iters = 0
        # print("Enter Anneal")
        while lowest_cost > 0:
            anneal_move = False
            # print("Iters: " + str(iters))
            # print("temp: " + str(temp))
            # print("Best Board: " + str(best_board))
            ttemp = max(temp * anneal_rate, 0.005)
            temp = ttemp
            self.run_steps +=1
            if iters > iterations:
                break

            while not anneal_move:
                if iters > iterations:
                    break
                iters += 1
                random_column = random.randint(0, n - 1)
                # random_queen_loc = self.main_board[random_column]
                random_new_loc = random.randint(0, n - 1)
                test_board = copy.deepcopy(best_board)
                test_board[random_column] = random_new_loc
                test_cost = self.total_cost(test_board)

                if test_cost < lowest_cost:
                    self.run_steps += 1
                    anneal_move = True
                    lowest_cost = test_cost
                    # print(best_board)
                    best_board = test_board
                    # print(best_board)
                    # print("Test Board: " + str(test_board))
                else:
                    d_e = test_cost - lowest_cost
                    cutoff = random.random()
                    boltz = math.exp(-d_e / temp)
                    if cutoff < boltz:
                        lowest_cost = test_cost
                        best_board = test_board
                        self.run_steps += 1
                        anneal_move = True
                    else:
                        continue

                    # print("Cutoff: " + str(cutoff))
                    # print("Boltz: " + str(math.exp(-d_e / temp)))
                    # print("Anneal Move: " + str(anneal_move))

        # self.main_board = best_board
        # self.cost = lowest_cost

        # for column_queen in range(n):  # Why can I not use current_game.size in place of n?
        #     # sa = self.current_game.start_board[column]
        #     for check_row_queen in range(n):  # Why can I not use current_game.size in place of n?
        #         if self.main_board[column_queen] == check_row_queen:  # reminder: board format [A, B, C, D, E, ..., Z] where the int of each item is the row
        #             for column in range(n):
        #                 for check_row in range(n):
        #                     if self.main_board[column] != check_row:
        #                         test_board = copy.deepcopy(self.main_board)
        #                         # new_queen = 0
        #                         test_board[column] = check_row
        #                         test_cost = self.total_cost(test_board)
        #                         if test_cost < lowest_cost:
        #                             self.run_steps += 1
        #                             lowest_cost = test_cost
        #                             best_board = test_board
        self.main_board = best_board
        self.cost = lowest_cost
        return

    def analysis(self):
        print("Total Boards: " + str(run_count))
        print("Total Solutions: " + str(self.solve_count))
        print("Avg. Steps for Solution: " + str(self.run_steps / run_count))
    #     best_moves = []
    #     best_cost = self.total_cost(current_game)
    #     for key, value in moves.iteritems():
    #         if value < best_cost:
    #             best_cost = value
    #         if key == best_cost:
    #             best_moves.append(key)
    #
    #     if len(best_moves):
    #         # randomly pick from tied best moves, could remove to meet HW requirements probably but I like this better
    #         chosen_move = random.randint(0, len(best_moves-1))
    #         column = best_moves[chosen_move][0]
    #         check_row = best_moves[chosen_move][1]
    #         current_game[column] = check_row
    #
    #     return

# GenerateBoard()
Action()
#     def analysis(self):
#         return
#
#
# def main():
#     random.seed()
#     main_board = Action(run_count)
#     main_board.analysis()
#
#
# if __name__ == "__main__":
#     main()
