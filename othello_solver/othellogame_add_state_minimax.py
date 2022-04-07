"""
Heuristics notes:
    - Gain corners
    - Avoid placing next to corner unless you own corner
    - Group onto owned corner pieces
    - Maximize number of legal moves
    - Minimize opponent legal moves
    - Frontier (exterior disks) not as good as internal
    - Playing in 'sweet 16' / closer to center is generally stronger
    - Have more disks at the end than the opposition
    - don't play immediately next to opposition on edges
    - balanced edge moves better (centered, 2,4,6)
"""

'''
othellogame module

sets up an Othello game closely following the book's framework for games

OthelloState is a class that will handle our state representation, then we've 
got stand-alone functions for player, actions, result and terminal_test

Differing from the book's framework, is that utility is *not* a stand-alone 
function, as each player might have their own separate way of calculating utility


'''
import copy
import random
import numpy

np = numpy


WHITE = 1
BLACK = -1
EMPTY = 0
SIZE = 8
SKIP = "SKIP"
BLACKWINS = 0
WHITEWINS = 0

class RandomPlayer:
    """Template class for an Othello Player

    An othello player *must* implement the following methods:

    get_color(self) - correctly returns the agent's color

    make_move(self, state) - given the state, returns an action that is the agent's move
    """

    def __init__(self, mycolor):
        self.color = mycolor

    def get_color(self):
        return self.color

    def make_move(self, state):
        curr_move = None
        legals = actions(state)[0]
        while curr_move is None:
            display(state)
            # if self.color == 1:
            #     print("White ", end='')
            # else:
            #     print("Black ", end='')
            # print(" to play.")
            # print("Legal moves are " + str(legals))
            # move = input("Enter your move as a r,c pair:")
            random_id = np.random.randint(0, len(legals))
            move = legals[random_id]
            print("Random Legals: " + str(legals))
            print("Random move: " + str(move))
            # if move == "":
            #     return legals[0]
            #
            if move == SKIP and SKIP in legals:
                return move
            if move in legals:
                curr_move = move
            else:
                print("That doesn't look like a legal action to me")
        return curr_move


class HeuristicPlayer:
    """Template class for an Othello Player

    An othello player *must* implement the following methods:

    get_color(self) - correctly returns the agent's color

    make_move(self, state) - given the state, returns an action that is the agent's move
    """

    def __init__(self, mycolor):
        self.color = mycolor

    def get_color(self):
        return self.color

    def make_move(self, state):
        curr_move = None
        legals = actions(state)[0]
        scores = actions(state)[1]
        while curr_move is None:
            display(state)
            # if self.color == 1:
            #     print("White ", end='')
            # else:
            #     print("Black ", end='')
            # print(" to play.")
            # print("Legal moves are " + str(legals))
            # move = input("Enter your move as a r,c pair:")
            """ replace the random_id function with a function that loops through all of the feasible moves and 
            utilizes the utility function to decide which move to make"""  # maybe this should be associated with each move as it is generated?
            # heuristic(state)
            if legals == ['SKIP']:
                move = SKIP
                return move
            if not scores:
                move = SKIP
                if move == SKIP and SKIP in legals:
                    return move

            print("heuristic legals: " + str(legals))
            print("heuristic scores: " + str(scores))
            max_score = max(scores)
            print("max_score: " + str(max_score))
            max_scores = []
            max_scores_index = []
            for _ in range(len(scores)):
                print(_)
                print("score: " + str(scores[_]))
                if scores[_] == max_score:
                    max_scores.append(scores[_])
                    max_scores_index.append(_)
                    print("max_scores_index: " + str(max_scores_index))
            if len(max_scores_index) == 1:
                move = legals[max_scores_index[0]]
            else:
                random_id = random.choice(max_scores_index)
                print("Rid: " + str(random_id))
                move = legals[random_id]
                print("Heuristic move: " + str(move))
            # if move == "":
            #     return legals[0]
            #

            if move in legals:
                curr_move = move
            else:
                print("That doesn't look like a legal action to me")
        return curr_move


class MinimaxPlayer:
    def __init__(self, mycolor, depth):
        self.color = mycolor
        self.depth = depth
        self.move = None
        self.v2 = 0

    # def minimax_play(self,state):
    #     move = 0
    #     while move <= self.depth:
    #         max(state)
    #         min(state)
    #         move += 1

    def maxi_move(self, state):
        move = None
        legals = actions(state)[0]
        # print("Type: " + str(type(state)))
    # print("max depth: " + str(self.depth))
    # print("legals: " + str(legals))
        # print("Maxi player: " + str(state.current))
        if legals == ['SKIP']:
            return heuristic(state), SKIP
        if self.depth == 0:
            # print("Maxi depth")
            # print(state.utility)
            return heuristic(state), None  # used to be state.utility

        v = -9999999
        self.depth -= 1
        for a in legals:
    # print("legals: " + str(len(legals)))
    # print("a-" + str(a))
            # self.depth -= 1 ??
            state.utility, a2 = self.mini_move(result(state, a))
    # print("v2: " + str(state.utility))
            if state.utility > v:
                # print("v2: " + str(state.utility))
                # print("v: " + str(v))
                v, move = state.utility, a
            # print("3>")
        self.depth += 1  # remove? testing only attempting to go back up tree
        return v, move

    def mini_move(self, state):
        # print(state.board_array)
        # state.current.get_color(self)
        ## print("legalsmini: " + str(actions(state[0])))
        # legals = actions(state)[0]
        # scores = actions(state)[1]
    # print("mini depth: " + str(self.depth))
        move = None
        legals = actions(state)[0]
    # print("legals: " + str(legals))
        # print("Mini player: " + str(state.current))  # players are switching properly
        # print("Mini board: " + str(state.board_array))  # board is filling out properly

        if self.depth == 0 or legals == ['SKIP']:
    # print("Mini depth")
            return heuristic(state), None
        v = 9999999
        self.depth -= 1
        for a in legals:
    # print("legals: " + str(len(legals)))
    # print("a-" + str(a))
            # self.depth -= 1 ??
            state.utility, a2 = self.maxi_move(result(state, a))
            # print("v2: " + str(state.utility))
            if state.utility < v:
                v, move = state.utility, a
            # print("4>")
        self.depth += 1  # remove? testing only attempting to go back up tree
        return v, move

    def get_color(self):
        return self.color

    def make_move(self, state):
        current_depth = -1
        minimax_score = 0
        curr_move = None
        legals = actions(state)[0]
        scores = actions(state)[1]
        curr_state = state

        while curr_move is None:
            display(state)
            # print("Here!!")
            # if self.color == 1:
            #     print("White ", end='')
            # else:
            #     print("Black ", end='')
            # print(" to play.")
            # print("Legal moves are " + str(legals))
            # move = input("Enter your move as a r,c pair:")
            """ replace the random_id function with a function that loops through all of the feasible moves and
            utilizes the utility function to decide which move to make"""  # maybe this should be associated with each move as it is generated?
            best_utility, move = MinimaxPlayer.maxi_move(self, state)
            if not scores:
                print("not scores")
                move = SKIP
                curr_move = move
                return curr_move
            if move == SKIP and SKIP in legals:
                curr_move = move
                return curr_move
            # print("BEST UTILITY: " + str(best_utility))
            # print("move: " + str(move))
            # print("heuristic legals: " + str(legals))
            # print("heuristic scores: " + str(scores))
            # max_score = max(scores)
            # print("max_score: " + str(max_score))
            # max_scores = []
            # max_scores_index = []
            # print("max_scores_index: " + str(max_scores_index))
            #
            # for _ in range(len(scores)):
            #     print(_)
            #     print("score: " + str(scores[_]))
            #     if scores[_] == max_score:
            #         print("scores[_]: " + str(scores[_]))
            #         max_scores.append(scores[_])
            #         max_scores_index.append(_)
            #         print("max_scores_index: " + str(max_scores_index))
            #         print(max_scores)
            # if len(max_scores_index) == 1:
            #     move = legals[max_scores_index[0]]
            # else:
            #     random_id = random.choice(max_scores_index)
            #     print("Rid: " + str(random_id))
            #     move = legals[random_id]
            #     print("Heuristic move: " + str(move))
            # # if move == "":
            # #     return legals[0]
            # #
            curr_move = move
            # if move in legals:
            #     curr_move = move
            # else:
            #     print("That doesn't look like a legal action to me")
        return curr_move


class ABPlayer:
    def __init__(self, mycolor, depth):
        self.color = mycolor
        self.depth = depth
        self.move = None

    # def minimax_play(self,state):
    #     move = 0
    #     while move <= self.depth:
    #         max(state)
    #         min(state)
    #         move += 1

    def ab_maxi_move(self, state, alpha, beta):
        move = None
        legals = actions(state)[0]
        # print("Type: " + str(type(state)))
    # print("max depth: " + str(self.depth))
    # print("legals: " + str(legals))
        # print("Maxi player: " + str(state.current))
        if legals == ['SKIP']:
            return heuristic(state), SKIP
        if self.depth == 0:
            # print("Maxi depth")
            # print(state.utility)
            return heuristic(state), None  # used to be state.utility

        v = -9999999
        self.depth -= 1
        for a in legals:
    # print("legals: " + str(len(legals)))
    # print("a-" + str(a))
            # self.depth -= 1 ??
            state.utility, a2 = self.ab_mini_move(result(state, a), alpha, beta)
    # print("v2: " + str(state.utility))
            if state.utility > v:
                # print("v2: " + str(state.utility))
                # print("v: " + str(v))
                v, move = state.utility, a
                alpha = max(alpha, v)
            # print("3>")
            if v >= beta:
                return v, move
        self.depth += 1  # remove? testing only attempting to go back up tree
        return v, move

    def ab_mini_move(self, state, alpha, beta):
        # print(state.board_array)
        # state.current.get_color(self)
        ## print("legalsmini: " + str(actions(state[0])))
        # legals = actions(state)[0]
        # scores = actions(state)[1]
    # print("mini depth: " + str(self.depth))
        move = None
        legals = actions(state)[0]
    # print("legals: " + str(legals))
        # print("Mini player: " + str(state.current))  # players are switching properly
        # print("Mini board: " + str(state.board_array))  # board is filling out properly
        if legals == ['SKIP']:
            return heuristic(state), SKIP
        if self.depth == 0:
    # print("Mini depth")
            return heuristic(state), None
        v = 9999999
        self.depth -= 1
        for a in legals:
    # print("legals: " + str(len(legals)))
    # print("a-" + str(a))
            # self.depth -= 1 ??
            state.utility, a2 = self.ab_maxi_move(result(state, a), alpha, beta)
            # print("v2: " + str(state.utility))
            if state.utility < v:
                v, move = state.utility, a
                beta = min(beta, v)
            if v <= alpha:
                return v, move
        self.depth += 1  # remove? testing only attempting to go back up tree
        return v, move

    def get_color(self):
        return self.color

    def make_move(self, state):
        curr_move = None
        legals = actions(state)[0]
        scores = actions(state)[1]
        alpha = -999999
        beta = 999999

        while curr_move is None:
            display(state)
            """ replace the random_id function with a function that loops through all of the feasible moves and
            utilizes the utility function to decide which move to make"""  # maybe this should be associated with each move as it is generated?
            best_utility, move = ABPlayer.ab_maxi_move(self, state, alpha, beta)
            if not scores:
                print("not scores")
                move = SKIP
                curr_move = SKIP
                return curr_move
            if move == SKIP and SKIP in legals:
                curr_move = move
                return curr_move

            curr_move = move
        return curr_move

# class OthelloPlayerTemplate:
#     '''Template class for an Othello Player
#
#     An othello player *must* implement the following methods:
#
#     get_color(self) - correctly returns the agent's color
#
#     make_move(self, state) - given the state, returns an action that is the agent's move
#     '''
#     def __init__(self, mycolor):
#         self.color = mycolor
#
#     def get_color(self):
#         return self.color
#
#     def make_move(self, state):
#         '''Given the state, returns a legal action for the agent to take in the state
#         '''
#         return None

class HumanPlayer:
    def __init__(self, mycolor):
        self.color = mycolor

    def get_color(self):
        return self.color

    def make_move(self, state):
        curr_move = None
        legals = actions(state)[0]
        while curr_move is None:
            display(state)
            if self.color == 1:
                print("White ", end='')
            else:
                print("Black ", end='')
            print(" to play.")
            print("Legal moves are " + str(legals))
            move = input("Enter your move as a r,c pair:")
            if move == "":
                return legals[0]
                print("break1")
            if move == SKIP and SKIP in legals:
                return move

            try:
                movetup = int(move.split(',')[0]), int(move.split(',')[1])
            except:
                movetup = None
            if movetup in legals:
                curr_move = movetup
            else:
                print("That doesn't look like a legal action to me")
        return curr_move


class OthelloState:
    '''A class to represent an othello game state'''

    def __init__(self, currentplayer, otherplayer, board_array=None, num_skips=0, utility=0):
        if board_array != None:
            self.board_array = board_array
        else:
            self.board_array = [[EMPTY] * SIZE for i in range(SIZE)]
            self.board_array[3][3] = WHITE
            self.board_array[4][4] = WHITE
            self.board_array[3][4] = BLACK
            self.board_array[4][3] = BLACK  # if board size changes these starting positions will get off-center
        self.num_skips = num_skips
        self.current = currentplayer
        self.other = otherplayer
        self.utility = utility
        # print("END OTHELLO STATE")


# def currentutility(state): # testing this, maybe should go in result.
#     return state.utility


def player(state):
    return state.current


def actions(state):
    '''Return a list of possible actions given the current state
    '''
    legal_actions = []
    scores = []
    # print("Self Color: " + str(state.current.get_color()))
    for i in range(SIZE):
        for j in range(SIZE):
            if result(state, (i, j)) != None:
                legal_actions.append((i, j))
                scores.append(result(state, (i, j)).utility)
                # print("scores: " + str(scores))
                # print("state.utility: " + str(state.utility))
                # print("Scores.append: " + str(state.utility))
    if len(legal_actions) == 0:
        legal_actions.append(SKIP)
    return legal_actions, scores


def result(state, action):
    # print("result action: " + str(action))
    # print("result state utility:" + str(state.utility))
    # print("result state array:" + str(state.board_array))

    '''Returns the resulting state after taking the given action

    (This is the workhorse function for checking legal moves as well as making moves)

    If the given action is not legal, returns None

    Add heuristic here? <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    return it to the new state and we can then loop this as the next step of the homework
    '''
    # first, special case! an action of SKIP is allowed if the current agent has no legal moves
    # in this case, we just skip to the other player's turn but keep the same board
    # print("Action 1: " + str(action))
    if action == SKIP:
        print(state.current)
        print("num skips: " + str(state.num_skips))
        newstate = OthelloState(state.other, state.current, copy.deepcopy(state.board_array),
                                state.num_skips + 1, state.utility)
        return newstate
    if state.board_array[action[0]][action[1]] != EMPTY:  # what does this do?
        return None
    color = state.current.get_color()
    # create new state with players swapped and a copy of the current board
    newstate = OthelloState(state.other, state.current, copy.deepcopy(state.board_array), state.num_skips, state.utility)

    newstate.board_array[action[0]][action[1]] = color

    flipped = False
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for d in directions:
        i = 1
        count = 0
        while i <= SIZE:
            x = action[0] + i * d[0]
            y = action[1] + i * d[1]
            if x < 0 or x >= SIZE or y < 0 or y >= SIZE:
                count = 0
                break
            elif newstate.board_array[x][y] == -1 * color:
                count += 1
            elif newstate.board_array[x][y] == color:
                break
            else:
                count = 0
                break
            i += 1

        if count > 0:
            flipped = True

        for i in range(count):
            x = action[0] + (i + 1) * d[0]
            y = action[1] + (i + 1) * d[1]
            newstate.board_array[x][y] = color

    if flipped:
        """ check Utility here"""  # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        newstate.utility = heuristic(newstate)
        return newstate
    else:
        # if no pieces are flipped, it's not a legal move
        return None


def heuristic(state):
    placement_weight = 10
    count_weight = 1
    frontier_weight = 5

    current_placement_score = 0
    other_placement_score = 0
    current_disk_count = 0
    other_disk_count = 0
    current_frontier_count = 0
    other_frontier_count = 0

    current_score = 0
    other_score = 0
    high_score = 0

    color = state.current.get_color()
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    p_weights = [(50, -20, 7, 5, 5, 7, -20, 50),
                 (-20, -50, -10, 5, 5, -10, -50, -20),
                 (10, -5, 5, 5, 5, -1, 5, 10),
                 (5, -2, -1, 5, 5, -1, -2, 5),
                 (5, -2, -1, 5, 5, -1, -2, 5),
                 (10, -5, 5, 5, 5, -1, 5, 10),
                 (-20, -50, -10, 5, 5, -10, -50, -20),
                 (50, -20, 7, 5, 5, 7, -20, 50)]
    # https://www.researchgate.net/figure/Position-value-of-each-cell-in-the-Othello-board_fig2_328458543

    for i in range(SIZE - 1):
        for j in range(SIZE - 1):
            if state.board_array[i][j] == color:
                current_disk_count += 1
                current_placement_score += p_weights[i][j]
            elif state.board_array[i][j] == -1 * color:
                other_disk_count += 1
                other_placement_score += p_weights[i][j]

            if state.board_array[i][j] != 0:
                for d in directions:
                    x = i + d[0]
                    y = j + d[1]
                    # print("(x, y) : (" + str(x) + "," + str(y) + ")")
                    # print(state.board_array[x][y])
                    if x < 0 or x >= SIZE - 1 or y < 0 or y >= SIZE - 1 and state.board_array[i][j != 0]:
                        break
                    elif state.board_array[x][y] == color:
                        current_frontier_count += 1
                    elif state.board_array[x][y] == -1 * color:
                        other_frontier_count += 1
                    else:
                        break

    current_score = (placement_weight * current_placement_score) \
                    + (count_weight * current_disk_count) \
                    + (frontier_weight * current_frontier_count)
    other_score = (placement_weight * other_placement_score) \
                  + (count_weight * other_disk_count) \
                  + (frontier_weight * other_frontier_count)
    high_score = current_score - other_score

    return high_score


def terminal_test(state):
    '''Simple terminal test
    '''
    # if both players have skipped
    if state.num_skips == 2:
        return True

    # if there are no empty spaces
    empty_count = 0
    for i in range(SIZE):
        for j in range(SIZE):
            if state.board_array[i][j] == EMPTY:
                empty_count += 1
    if empty_count == 0:
        return True
    return False


def display(state):
    '''Displays the current state in the terminal window
    '''
    print('  ', end='')
    for i in range(SIZE):
        print(i, end='')
    print()
    for i in range(SIZE):
        print(i, '', end='')
        for j in range(SIZE):
            if state.board_array[j][i] == WHITE:
                print('W', end='')
            elif state.board_array[j][i] == BLACK:
                print('B', end='')
            else:
                print('-', end='')
        print()


def display_final(state):
    '''Displays the score and declares a winner (or tie)
    '''
    wcount = 0
    bcount = 0
    global WHITEWINS
    global BLACKWINS
    for i in range(SIZE):
        for j in range(SIZE):
            if state.board_array[i][j] == WHITE:
                wcount += 1
            elif state.board_array[i][j] == BLACK:
                bcount += 1

    print("Black: " + str(bcount))
    print("White: " + str(wcount))
    if wcount > bcount:
        print("White wins")
        WHITEWINS += 1
    elif wcount < bcount:
        print("Black wins")
        BLACKWINS += 1
    else:
        print("Tie")


def play_game(p1=RandomPlayer(BLACK), p2=HeuristicPlayer(WHITE)):
    '''Plays a game with two players. By default, uses two humans
    '''
    white_wins = 0
    black_wins = 0
    if p1 == None:
        p1 = HumanPlayer(BLACK)
    if p2 == None:
        p2 = HumanPlayer(WHITE)

    s = OthelloState(p1, p2)
    while True:
        action = p1.make_move(s)
        if action not in actions(s)[0]:
            # print("Break Action: " +str(actions(s).type))
            # print("Break Action: " +str(action.type))
            print("Illegal move made by Black")
            print("White wins!")
            white_wins += 1
            return white_wins
        s = result(s, action)
        if terminal_test(s):
            print("Game Over")
            display(s)
            display_final(s)
            return
        action = p2.make_move(s)
        if action not in actions(s)[0]:
            print("Illegal move made by White")
            print("Black wins!")
            black_wins += 1
            return black_wins
        s = result(s, action)
        if terminal_test(s):
            print("Game Over")
            display(s)
            display_final(s)
            return


def main():
    i = 0
    global BLACKWINS, WHITEWINS
    while i < 100:
        play_game()
        i += 1
    print("black wins: " + str(BLACKWINS) + " white wins: " + str(WHITEWINS))
    return

if __name__ == '__main__':
    main()
