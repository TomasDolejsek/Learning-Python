import os.path
import logging

class Flashcards:
    def __init__(self):
        self.deck = dict()

    def add_card(self):
        print("The card:")
        while True:
            card = input()
            if card in self.deck.keys():
                print(f"The card \"{card}\" already exists. Try again:")
                continue
            else:
                break
        print("The definition of the card:")
        while True:
            definition = input()
            if definition in self.deck.values():
                print(f"The definition \"{definition}\" already exists. Try again:")
                continue
            else:
                break
        self.deck[card] = [definition, '0']
        print(f"The pair (\"{card}\": \"{definition}\") has been added.\n")

    def remove_card(self):
        which = input("Which card?\n")
        if which not in self.deck.keys():
            print(f"Can't remove \"{which}\": there is no such card.\n")
        else:
            del self.deck[which]
            print("The card has been removed.\n")

    def import_from_file(self):
        filename = input("File name:\n")
        if not os.path.exists(filename):
            print("File not found.\n")
        else:
            file = open(filename, "r")
            lines = file.read().splitlines()
            for card in lines:
                card = card.split(':')
                self.deck[card[0]] = [card[1], card[2]]
            file.close()
            print(f"{len(lines)} cards have been loaded.\n")

    def export_to_file(self):
        lines = ''
        filename = input("File name:\n")
        file = open(filename, "w")
        for card, backside in self.deck.items():
            lines += f"{card}:{backside[0]}:{backside[1]}\n"
        file.write(lines)
        file.close()
        print(f"{len(self.deck.keys())} cards have been saved.\n")

    def ask_player(self):
        counter = 0
        while True:
            try:
                howmany = int(input("How many times to ask?\n"))
                if howmany <= 0:
                    raise ValueError
                else:
                    break
            except ValueError:
                print("You should enter a number > 0")
                continue
        while True:
            if counter == howmany:
                break
            for card, backside in self.deck.items():
                answer = input(f"Print the definition of \"{card}\":\n")
                if answer == backside[0]:
                    print("Correct!")
                else:
                    print(f"Wrong. The right answer is \"{backside[0]}\"", end='')
                    self.deck[card] = [self.deck[card][0], str(int(self.deck[card][1]) + 1)]
                    searched_key = [k for k, v in self.deck.items() if v[0] == answer]
                    if searched_key:
                        print(f", but your definition is correct for \"{searched_key[0]}\"")
                    else:
                        print()
                counter += 1
                if counter == howmany:
                    break

    def hardest_card(self):
        maximum = max([int(v[1]) for v in self.deck.values()])
        if maximum > 0:
            searched_keys = [k for k, v in self.deck.items() if int(v[1]) == maximum]
            print(f"The hardest card{'s are' if len(searched_keys) > 1 else ' is'} \"", end='')
            print(*searched_keys, sep='", "', end='')
            print(f"\". You have {maximum} error{'s' if maximum > 1 else ''} answering it.\n")
        else:
            print("There are no cards with errors.")

    def reset_stats(self):
        for card, backside in self.deck.items():
            self.deck[card] = [backside[0], '0']
        print("Card statistics have been reset.")

class MainMenu:
    def __init__(self):
        self.valid_commands = ('add', 'remove', 'import', 'export', 'ask',
                               'exit', 'log', 'hardest card', 'reset stats'
                               )
        self.start()

    def start(self):
        game = Flashcards()
        while True:
            print("Input the action (", end='')
            print(*self.valid_commands, sep=', ', end='')
            print("):")
            user = input().lower()
            if not user:
                continue
            if user not in self.valid_commands:
                print("Unknown command.")
                continue
            if user == self.valid_commands[0]:
                game.add_card()
                continue
            if user == self.valid_commands[1]:
                game.remove_card()
                continue
            if user == self.valid_commands[2]:
                game.import_from_file()
                continue
            if user == self.valid_commands[3]:
                game.export_to_file()
                continue
            if user == self.valid_commands[4]:
                game.ask_player()
                continue
            if user == self.valid_commands[5]:
                print("Bye bye!")
                exit()
            if user == self.valid_commands[7]:
                game.hardest_card()
                continue
            if user == self.valid_commands[8]:
                game.reset_stats()
                continue


if __name__ == '__main__':
    MainMenu()
