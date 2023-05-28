# Project_004
# Author: TDO
# Date: 2023-04-20
# Name: Hangman Game
# Task: The user will have to guess an alphabet to complete a word, and also each user will have a limited number of chances to guess a letter.
# The programmer can create the preorganized list of words to be finished and then include a specific function to check whether the user has guessed the correct letter.
# If yes then include that letter to word for finishing the default word and if the guesswork is not true then reducing the count of chances to guess further.

import random

print ("*** Hangman Game ***")

words = ["ironman" , "hulk" , "thor" , "captainamerica" , "clint" , "loki" , "avengers" , "nick" , "phil" , "maria"]  # list of possible words to guess
picked_letters = list()  # list of letters picked by user
hangman = list()  # picture of hangman
next_round = True  # False = game over
fattemps = 0  # number of failed attemps
secret_word = ''  # that's the word that user tries to guess
hint_word = ''  # searched word with guessed letters (other letters = -)

def new_game():  # clears all variables and generates random word from the list + print some text
    global picked_letters, hangman, next_round, fattemps, secret_word, hint_word
    picked_letters.clear()
    hangman.clear()
    next_round = True
    fattemps = 0
    secret_word = random.choice(words)  # random pick
    hint_word = ''
    for i in range(len(secret_word)):
        hint_word += ('-')
    
    print()
    print("Try to guess one of the following words:")
    print(words)
    print("Let's start.")
    print("Random word has been picked.")
    print_hangman(fattemps)
        
def act_hangman(step):  # actualize hangman picture according to number of attemps
    global hangman
    if step == 0:
        hangman.append("  --------  ")
    elif step == 1:
        hangman.append("     O      ")
    elif step == 2:
        hangman.append("     |      ")
    elif step == 3:
        hangman.append("    /       ")
    elif step == 4:
        hangman[3] = ("    / \     ")
    elif step == 5:
        hangman[1] = ("   \ O      ")
    elif step == 6:
        hangman[1] = ("   \ O /    ")
    elif step == 7:
        hangman[1] = ("   \ O /|   ")
    elif step == 8:
        hangman[1] = ("   \ O_|/   ")
    else:
        hangman[1] = ("     O_|    ")
        hangman[2] = ("    /|\     ")
        
def print_hangman(step):  # prints info text and hangman
    act_hangman(step)
    print()
    print(f"You have {9-step} turns left.")
    if step == 8:
        print("Last breaths counting, take care!")
    elif step == 9:
        print("You let a kind man die.")
        print("GAME OVER!")
    for i in range(len(hangman)):
        print(hangman[i])

def pick_letter():  # input + input check
    letter = ''
    while not letter.isalpha() or letter in picked_letters:  # input check
        print("Please pick a letter: ", end = '')
        letter = input().lower()
        if not letter.isalpha():  # wrong input
            print("That's not a letter!")
        elif letter in picked_letters:  # user already chose this letter before
            print("You already chose that letter!")
        else:
            picked_letters.append(letter)  # let's note which letters has been already picked
            break
    return letter

def print_hint():  # prints the hint_word and letter picked so far
    print(f"What is this word? >>> {hint_word}")
    print(f"So far you've picked these letters: {sorted(picked_letters)}")
    
def play_a_round(letter):  # let's play one round
    global fattemps, hint_word
    print()
    if letter in secret_word:
        print("Good choice!")
        for i in range(len(secret_word)):  # update of hint_word
            if letter == secret_word[i]:
                hint_word = hint_word[:i] + secret_word[i] + hint_word[i+1:]
    else:
        print("Bad choice!")
        fattemps += 1
        print_hangman(fattemps)
            
    if hint_word == secret_word:
        print(f"You win! You found the secret word '{secret_word}'.")
        return False
    else:
        return True

# main program
while True:
    new_game()
    while next_round == True and fattemps < 9:
        print_hint()
        picked = pick_letter()
        next_round = play_a_round(picked)
    print()
    print("Do you want to play a new game? y/n")
    if input().lower() != 'y':
        break