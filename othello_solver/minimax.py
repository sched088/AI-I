# python-like pseudocode for minimax

def minimax_search(game, state):
    global PLAYER # >:(   boo globals!!! angry face
    player = game.to_move(state)
    val, move = max_value(game, state)
    return move

def max_value(game, state):
    if game.is_terminal(state):
        return game.utility(state, PLAYER), None
    v, move = -inf, None
    for a in game.actions(state):
        v2, a2 = min_value(game, game.result(state, a))
        if v2 > v:
            v, move = v2, a
    return v, move

def min_value(game, state):
    if game.is_terminal(state):
        return game.utility(state, PLAYER), None
    v, move = inf, None
    for a in game.actions(state):
        v2, a2 = max_value(game, game.result(state, a))
        if v2 < v:
            v, move = v2, a
    return v, move


def ab_max_value(game, state, alpha, beta):
    # after v,move = v2, a
    #       alpha = max(alpha, v)
    # outside if, but still in loop
    #   if v >= beta: return v, move

def ab_min_value(game, state, alpha, beta):
    # after v, move = v2, a
    #       beta = min(beta, v)
    # outside if, but still in loop
    #   if v <= alpha: return v, move

function minimax(node, depth, maximizingPlayer) is
    if depth = 0 or node is a terminal node then
    return the heuristic value of node
    if maximizingPlayer then
        value := −∞
        for each child of node do
            value := max(value, minimax(child, depth − 1, FALSE))
        return value
    else (*minimizing player *)
        value := +∞
        for each child of node do
            value := min(value, minimax(child, depth − 1, TRUE))
        return value