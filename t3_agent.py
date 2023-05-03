import json
import random
import t3_engine as engine

class Agent:

    def __init__(self, symbol, training = False, exploration = 0.1, learning_rate = 0.1, state_table = {}, model_name = "model.json"):
        self.symbol = symbol
        self.exploration = exploration
        self.learning_rate = learning_rate
        self.state_table = state_table
        self.model_name = model_name
        self.training = training
        self.oldBoard = engine.get_initial_board()

    # return either the move with the highest value, 
    # a random move with probability exploration 
    # or -1 if no move is possible
    def get_next_move(self, board):
        emptyFields = [i for i in range(len(board)) if board[i].isspace()]
        emptyFields = [i+1 for i in emptyFields]
        bestMove = -1
        bestValue = -1

        if(emptyFields.count == 0): return bestMove
        if(self.training):
            if(random.random() < self.exploration): return random.choice(emptyFields) # exploration

        for field in emptyFields:
            currentBoard = engine.insert_symbol(board, self.symbol, field)

            if currentBoard in self.state_table:
                currentValue = self.state_table[currentBoard]
            else:
                self.state_table[currentBoard] = currentValue = 0.5
            
            if(currentValue > bestValue):
                bestValue = currentValue 
                bestMove = field
        
        return bestMove

    # updates values in the state table
    def update_value(self, S_t1):
        S_t = self.oldBoard
        result = engine.evaluate(S_t1)
        if(result[0] == True):
            if(result[1] == self.symbol):
                self.state_table[S_t1] = 1
            else:
                self.state_table[S_t1] = 0

        if S_t in self.state_table and S_t1 in self.state_table:
            self.state_table[S_t] = self.state_table[S_t] + self.learning_rate * (self.state_table[S_t1] - self.state_table[S_t])
        self.oldBoard = S_t1

    def export_model(self):
        with open(self.model_name, "w") as outfile:
            json.dump(self.state_table, outfile)


    
def load_model(filename):
    with open(filename) as infile:
        model = json.load(infile)
    return model
    