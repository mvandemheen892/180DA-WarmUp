import random as rndm

def AIMove():
    possible_moves=['rock','paper','scissors']
    random_index=rndm.randint(0,2)
    return possible_moves[random_index]

def GetPlayerMove():
    user_move=input("What is your choice?\n")
    if user_move == 'rock' or user_move == 'paper' or user_move == 'scissors':
        return user_move
    else:
        print("That's not a valid choice, try again!")
        GetPlayerMove()

def whoWon(player1move,player2move):
    if player1move == player2move :
        #tie
        return 0
    elif (player1move == 'rock' and player2move =='scissors') or (player1move == "paper" and player2move == "rock") or (player1move == 'scissors' and player2move == 'paper'):
        return 1
    else:
        return 2

print("Welcome to Rock, Paper, Scissors Virtual Edition")

while True:
    
    player_move = GetPlayerMove()
    AI_move = AIMove()
    winner = whoWon(player_move,AI_move)
    if winner == 0:
        print("You guys both put " + player_move + ", its a tie!")
        continue
    elif winner == 1:
        print("The Computer chose " + AI_move + ", so you win!")
        continue
    elif winner == 2:
        print("The Computer chose " + AI_move + ", so you lose!")


