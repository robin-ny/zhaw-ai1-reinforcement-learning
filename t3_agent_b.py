import json
import random
import t3_engine as engine


exploration = 0.1
learning_rate = 0.1


def init(val):
    global temp
    global pc
    pc = val
    temp = {'         ':0.5}
    
# return either the move with the highest value, 
# a random move with probability exploration 
# or -1 if no move is possible
def get_next_move(board, player):
    emptyFields = [i for i in range(len(board)) if board[i].isspace()]
    emptyFields = [i+1 for i in emptyFields]
    bestMove = -1
    bestValue = -1

    if(emptyFields.count == 0): return bestMove  
    if(random.random() < exploration): return random.choice(emptyFields) # exploration

    for field in emptyFields:
        currentBoard = engine.insert_symbol(board, player, field)

        if currentBoard in temp:
            currentValue = temp[currentBoard]
        else:
            temp[currentBoard] = currentValue = 0.5
        
        if(currentValue > bestValue):
            bestValue = currentValue 
            bestMove = field
    
    return bestMove

def set_terminal_value(S_t1):
    result = engine.evaluate(S_t1)
    if(result[0] == True):
        if(result[1] == pc):
            temp[S_t1] = 1
        else:
            temp[S_t1] = 0

# updates values in the state table
def update_value(S_t, S_t1):
    if S_t in temp and S_t1 in temp:
        temp[S_t] = temp[S_t] + learning_rate * (temp[S_t1] - temp[S_t])

def export_model():
    with open("model_b.json", "w") as outfile:
        json.dump(temp, outfile)


### COMPETITIVE MODE ###
def load_model(filename):
    with open(filename) as infile:
        model = json.load(infile)
    return model


def get_best_action(board, model, turn):
    emptyFields = [i for i in range(len(board)) if board[i].isspace()]
    [i+1 for i in emptyFields]

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
    
    return bestMove+1