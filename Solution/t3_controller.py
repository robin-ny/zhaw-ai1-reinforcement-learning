# -*- coding: utf-8 -*-
"""
Tic-Tac-Toe controller TEMPLATE

Autor: stdm
Creation: Feb 14, 2018

"""

import random
#TODO: import t3_agent as agent # <- implement and include your own learning agent
import t3_engine as engine
from t3_agent import Agent, load_model


#Some definitions to configure the behaviour of this controller
training_mode = False
model_file_name = "model.json"

#control both training and playing
def main():

    random.seed()
    
    print('Welcome to the Tic-Tac-Toe self-play RL agent environment.')
    engine.print_help()

    #train a RL agent by self-play
    if training_mode:
        try:
            agent = Agent('X',training_mode,model_name="agent.json",state_table={})
            opponent = Agent('O',training_mode,model_name="opponent.json",state_table={})
            gamesPlayed = 1
            board = engine.get_initial_board()
            playerOrder = engine.randomize_player_order()
            while True:
                turn = engine.whos_turn(board, playerOrder)
                if turn=='X':             
                    field = agent.get_next_move(board)
                    board = engine.make_move(board, field, turn)
                    agent.update_value(board)
                    assert(board!='')
                else: #get player's input (until valid) and make the respective move
                    field = opponent.get_next_move(board)
                    board = engine.make_move(board, field, turn)
                    opponent.update_value(board)
                    assert(board!='')

                #print new state, evaluate game
                game_over, who_won, reward = engine.evaluate(board)
                #engine.print_board(board, False)
                
                if game_over:
                    print('The game ' + str(gamesPlayed) + ' is over. ' + who_won + ' won.')
                    gamesPlayed += 1
                    agent.update_value(board)
                    opponent.update_value(board)
                    board = engine.get_initial_board()
                    agent.oldBoard = board
                    opponent.oldBoard = board
                    playerOrder = engine.randomize_player_order()

        except KeyboardInterrupt:
            agent.export_model()
            opponent.export_model()
            



    #apply a trained RL agent in a game aghainst a human
    else: #training_mode==False
        board = engine.get_initial_board()
        playerOrder = engine.randomize_player_order()
        model = load_model("./agent.json")
        agent = Agent('X',training_mode,state_table=model)
        print('You are player O, ' + playerOrder[0] + ' starts!')
        
        while True:
            turn = engine.whos_turn(board, playerOrder)
            if turn=='X': #get the agent's input, make the respective move                
                field = agent.get_next_move(board) # <- API to fulfill by own agent implementation: return the best possible move (field# 1-9, according to learnt model) in the given state; the board has a format specified in t3_engine.py
                board = engine.make_move(board, field, turn)
                assert(board!='')
            else: #get player's input (until valid) and make the respective move
                while True: 
                    field = input("Which field to set? ")
                    if(engine.make_move(board, field, turn) !='') :
                        board = engine.make_move(board, field, turn)
                        break
            
            #print new state, evaluate game
            print('Game after ' + turn + "'s move: ")
            engine.print_board(board, False)
            game_over, who_won, reward = engine.evaluate(board)
            
            if game_over:
                print('The game is over. ' + who_won + ' won.')
                break

    return # end of main()


# start the script if executed directly    
if __name__ == '__main__':
    
    main()
