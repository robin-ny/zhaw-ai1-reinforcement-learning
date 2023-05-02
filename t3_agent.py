import random
import t3_engine as engine
import t3_states as state

exploration = 0.1
learning_rate = 0.05
    
# return either the move with the highest value, 
# a random move with probability exploration 
# or -1 if no move is possible
def get_next_move(board, player):
    emptyFields = [i for i in range(len(board)) if board[i].isspace()]
    bestMove = -1
    bestValue = -1

    if(emptyFields.count == 0): return bestMove  
    if(random.random() < exploration): return random.choice(emptyFields) # exploration

    for field in emptyFields:
        currentBoard = engine.insert_symbol(board, player, field)

        if currentBoard in state.table:
            currentValue = state.table[currentBoard]
        else:
            state.table[currentBoard] = currentValue = 0.5
        
        if(currentValue > bestValue):
            bestValue = currentValue 
            bestMove = field
    
    return bestMove

def set_terminal_value(S_t1, player):
    result = engine.evaluate(S_t1)
    if(result[0] == True):
        if(result[1] == player):
            state.table[S_t1] = 1
        else:
            state.table[S_t1] = 0

# updates values in the state table
def update_value(S_t, S_t1):
    if S_t in state.table and S_t1 in state.table:
        state.table[S_t] = state.table[S_t] + learning_rate * (state.table[S_t1] - state.table[S_t])



### COMPETITIVE MODE ###
def load_model(filename):
    state.import_model(filename)


def get_best_action(board, model, turn):
    emptyFields = [i for i in range(len(board)) if board[i].isspace()]

    bestMove = -1
    bestValue = -1

    if(emptyFields.count == 0): return bestMove

    for field in emptyFields:
        currentBoard = engine.insert_symbol(board, turn, field)

        if currentBoard in model.table:
            currentValue = model.table[currentBoard]
        else:
            model.table[currentBoard] = currentValue = 0.5
        
        if(currentValue > bestValue):
            bestValue = currentValue 
            bestMove = field
    
    return bestMove