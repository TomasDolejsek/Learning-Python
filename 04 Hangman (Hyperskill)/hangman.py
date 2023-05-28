import random

# variables
words = ['python', 'java', 'swift', 'javascript']
menu = ['play','results','exit']  # menu choices
pchoice = ''  # what did player pick in menu
letter = ''  # player's input
wins = 0  # how many times did player win
loses = 0  # how many times did player lose

# main code
print("H A N G M A N")

while True:  # endless loop
    pchoice = input("Type \"play\" to play the game, \"results\" to show the scoreboard, and \"exit\" to quit: ")
    
    if pchoice not in menu:  # wrong menu choice
        continue
    if pchoice == 'results':  # display results
        print(f"You won: {wins} times.")
        print(f"You lost: {loses} times.")
        continue
    if pchoice == 'exit':  # game over
        break
    
    # only 'play' option remains - let's play then
    # first we must reset variables for the new game
    attemps = 8
    rnd_word = random.choice(words)
    hint_word = '-' * len(rnd_word)
    already_guessed = set()
    while attemps > 0:
        print("\n" + hint_word)
        letter = input("Input a letter: ")
    
        # testing input
        if len(letter) != 1:
            print("Please, input a single letter.")
            continue
        if not letter.isalpha() or not letter.islower():
            print("Please, enter a lowercase letter from the English alphabet.")
            continue

        # already guessed?
        if letter in already_guessed:
            print("You've already guessed this letter.")
            continue
        else:
            already_guessed.add(letter)
    
        # right letter?
        if letter in rnd_word:
            for i in range(len(rnd_word)):
                if letter == rnd_word[i]:
                    hint_word = hint_word[:i] + letter + hint_word[i + 1:]           
        else:
            attemps -= 1
            print("That letter doesn't appear in the word.")
            continue
    
        # player wins
        if hint_word == rnd_word:
            wins += 1
            print(f"You guessed the word {hint_word}!")
            print("You survived!")
            break
    else:  # player loses
        loses += 1
        print("You lost!")