# Project_002
# Author: TDO
# Date: 2023-04-19
# Name: Dice Rolling Simulator
# Task: This python project will generate a random number each time the dice is rolled and also the user can repeat this program as long as he wants. The program is projected in such a way that when the user rolls a die,
# the program will generate a random number between 1 and 6. The program will use the in-build function to generate the random number for rolling dice. It will also ask the user if they wish to roll the dice again.

import random

print("*** Dice Rolling Simulator ***")

next_roll = True # must be True to enter the while loop at least one time

while next_roll == True:
    if input("""Do you want to roll a dice? Press [y]es or [n]o: """) != 'y':
        print("Game over.")
        next_roll = False
        continue
    else:
        next_roll=True
    
    rolled_number=random.randint(1,6)
    
    if rolled_number == 1: 
        print("[-----]") 
        print("[     ]") 
        print("[  0  ]") 
        print("[     ]") 
        print("[-----]") 
    elif rolled_number == 2: 
        print("[-----]") 
        print("[ 0   ]") 
        print("[     ]") 
        print("[   0 ]") 
        print("[-----]") 
    elif rolled_number == 3: 
        print("[-----]") 
        print("[     ]") 
        print("[0 0 0]") 
        print("[     ]") 
        print("[-----]") 
    elif rolled_number == 4: 
        print("[-----]") 
        print("[0   0]") 
        print("[     ]") 
        print("[0   0]") 
        print("[-----]") 
    elif rolled_number == 5: 
        print("[-----]") 
        print("[0   0]") 
        print("[  0  ]") 
        print("[0   0]") 
        print("[-----]") 
    else: 
        print("[-----]") 
        print("[0 0 0]") 
        print("[     ]") 
        print("[0 0 0]") 
        print("[-----]")

    

