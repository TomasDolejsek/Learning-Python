# Project_003
# Author: TDO
# Date: 2023-04-20
# Name: Rock, Paper, Scissors Game
# Task: In this program, we will use a random function for generating the random output by the computer side. The user will make the first move and then the program makes one.
# Then a function will check the validity of the move. At last, we will display the result and ask the user to play again or not.

from random import randint  #only randint function is needed

print("*** Rock - Paper - Scissors Game ***")

play_options = ['Rock','Paper','Scissors','Quit']  # universal list of play options; can be changed but the order must remain the same to fulfill logic of the game. Quit must be always the last option.
choices = list()  # possible player's inputs

next_round = True  # should we play next round?
player = ''  # player's choice
pchoice = 0  # index of picked option
cchoice = 0  # computer's choice (random number)
games = 0  # games played
pwin = 0  # player wins
cwin = 0  # computer wins
ties = 0  # ties

# generating a list of possible player choices
for i in range(len(play_options)):
    choices.append(play_options[i][0].upper())  # upper() to be more flexible
    
# starting the game
while next_round == True:
    while player not in choices:  # input check
        print("Your pick? ", end = '')
        for i in range(len(play_options)):
            print(f"[{play_options[i][0]}]{play_options[i][1:len(play_options[i]) + 1]} ", end = '')
        print(">>> ", end = '')
        player = input().upper()  # player has picked
                  
        if player not in choices:
            print("Please enter one of the letters within [].")
        else:
             pchoice = choices.index(player)
        
    if player == choices[-1]:
        next_round = False
        print (f"Game over. We played {games} game(s). You won {pwin}x, computer won {cwin}x, ties = {ties}.")
        continue
   
    cchoice = randint(0,len(choices) - 2)  # random pick
        
    # outcome of the game decision
    games += 1
    print(f"You picked {play_options[pchoice]}. Computer picked {play_options[cchoice]}. ", end = '')
    if pchoice == cchoice:
        ties += 1
        print("It's a tie!")
    elif pchoice == 0:
        if cchoice == 1:
            cwin += 1
            print(f"{play_options[cchoice]} cowers {play_options[pchoice]}. Computer wins!")
        else:
            pwin +=1
            print(f"{play_options[pchoice]} smashes {play_options[cchoice]}. You win!")
    elif pchoice == 1:
        if cchoice == 0:
            pwin += 1
            print(f"{play_options[pchoice]} cowers {play_options[cchoice]}. You win!")
        else:
            cwin += 1
            print(f"{play_options[cchoice]} cut {play_options[pchoice]}. Computer wins!")
    else:
        if cchoice == 0:
            cwin +=1
            print(f"{play_options[cchoice]} smashes {play_options[pchoice]}. Computer wins!")
        else:
            pwin += 1
            print(f"{play_options[pchoice]} cut {play_options[cchoice]}. You win!")
    player = ''  # erased for the next game
            