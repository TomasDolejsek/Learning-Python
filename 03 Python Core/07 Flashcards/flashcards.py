import os.path
import logging
from io import StringIO
import argparse


class Logger:
    def __init__(self):
        self.log_output = logging.getLogger('Output')
        self.log_output.setLevel(logging.INFO)
        self.log_capture_string = StringIO()
        ch = logging.StreamHandler(self.log_capture_string)
        formatter = logging.Formatter('%(asctime)s - %(name)s: %(message)s')
        ch.setFormatter(formatter)
        self.log_output.addHandler(ch)
        self.log_input = logging.getLogger('Input')
        self.log_input.setLevel(logging.INFO)
        self.log_input.addHandler(ch)

    # print to stdout + log
    def printl(self, text):
        print(text)
        self.log_output.info(text)

    # ask for input from stdin + log
    def inputl(self):
        user = input()
        self.log_input.info(user)
        return user


class Flashcards:
    def __init__(self):
        self.deck = dict()

    def add_card(self):
        logger.printl("The card:")
        while True:
            card = logger.inputl()
            if card in self.deck.keys():
                logger.printl(f"The card \"{card}\" already exists. Try again:")
                continue
            else:
                break
        logger.printl("The definition of the card:")
        while True:
            definition = logger.inputl()
            def_list = [v[0] for v in self.deck.values()]
            if definition in def_list:
                logger.printl(f"The definition \"{definition}\" already exists. Try again:")
                continue
            else:
                break
        self.deck[card] = [definition, '0']
        logger.printl(f"The pair (\"{card}\": \"{definition}\") has been added.")

    def remove_card(self):
        logger.printl("Which card?")
        which = logger.inputl()
        if which not in self.deck.keys():
            logger.printl(f"Can't remove \"{which}\": there is no such card.")
        else:
            del self.deck[which]
            logger.printl("The card has been removed.")

    def import_from_file(self):
        logger.printl("File name:")
        filename = logger.inputl()
        self.import_cards(filename)

    def import_cards(self, filename):
        if not os.path.exists(filename):
            logger.printl(f"{filename} File not found.")
            return
        with open(filename, 'r') as file:
            lines = file.read().splitlines()
            for card in lines:
                card = card.split(':')
                self.deck[card[0]] = [card[1], card[2]]
            logger.printl(f"{len(lines)} card{'s have' if len(lines) > 1 else ' has'} been loaded.")

    def export_to_file(self):
        logger.printl("File name:")
        filename = logger.inputl()
        self.export_cards(filename)

    def export_cards(self, filename):
        lines = ''
        with open(filename, "w") as file:
            for card, backside in self.deck.items():
                lines += f"{card}:{backside[0]}:{backside[1]}\n"
            file.write(lines)
        logger.printl(f"{len(self.deck.keys())} card{'s have' if len(self.deck.keys()) > 1 else ' has'} been saved.")

    def ask_player(self):
        counter = 0
        while True:
            try:
                logger.printl("How many times to ask?")
                howmany = int(logger.inputl())
                if howmany <= 0:
                    raise ValueError
                else:
                    break
            except ValueError:
                logger.printl("You should enter a number > 0")
                continue
        while True:
            if counter == howmany:
                break
            for card, backside in self.deck.items():
                logger.printl(f"Print the definition of \"{card}\":")
                answer = logger.inputl()
                if answer == backside[0]:
                    text = "Correct!"
                else:
                    text = f"Wrong. The right answer is \"{backside[0]}\""
                    self.deck[card] = [self.deck[card][0], str(int(self.deck[card][1]) + 1)]
                    searched_key = [k for k, v in self.deck.items() if v[0] == answer]
                    if searched_key:
                        text += f", but your definition is correct for \"{searched_key[0]}\""
                logger.printl(text)
                counter += 1
                if counter == howmany:
                    break

    def hardest_card(self):
        maximum = max([int(v[1]) for v in self.deck.values()]) if len(self.deck) > 0 else 0
        if maximum > 0:
            searched_keys = [k for k, v in self.deck.items() if int(v[1]) == maximum]
            text = f"The hardest card{'s are' if len(searched_keys) > 1 else ' is'} \""
            text += '", "'.join(searched_keys)
            text += f"\". You have {maximum} error{'s' if maximum > 1 else ''} answering it."
        else:
            text = "There are no cards with errors."
        logger.printl(text)

    def reset_stats(self):
        for card, backside in self.deck.items():
            self.deck[card] = [backside[0], '0']
        logger.printl("Card statistics have been reset.")

    def save_log(self):
        logger.printl("File name:")
        filename = logger.inputl()
        logger.printl("The log has been saved.")
        log_content = logger.log_capture_string.getvalue()
        with open(filename, 'w') as file:
            file.write(log_content)


class MainMenu:
    def __init__(self, filein, fileout):
        self.valid_commands = ('add', 'remove', 'import', 'export', 'ask',
                               'exit', 'log', 'hardest card', 'reset stats'
                               )
        self.filein = filein
        self.fileout = fileout
        self.start()

    def start(self):
        game = Flashcards()
        if self.filein:
            game.import_cards(self.filein)
        while True:
            logger.printl("Input the action (" + ', '.join(self.valid_commands) + "):")
            user = logger.inputl()
            if not user:
                continue
            if user not in self.valid_commands:
                logger.printl("Unknown command.")
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
                logger.printl("Bye bye!")
                if self.fileout:
                    game.export_cards(self.fileout)
                exit()
            if user == self.valid_commands[6]:
                game.save_log()
                continue
            if user == self.valid_commands[7]:
                game.hardest_card()
                continue
            if user == self.valid_commands[8]:
                game.reset_stats()
                continue


class CommandLine:
    def __init__(self):
        parser = argparse.ArgumentParser(description='Flashcards')
        parser.add_argument('--import_from')
        parser.add_argument('--export_to')
        self.args = parser.parse_args()
        self.arglist = list(vars(self.args).values())  # list of input values

    def get_arguments(self):
        return self.arglist[0], self.arglist[1]


if __name__ == '__main__':
    logger = Logger()
    command_line = CommandLine()
    MainMenu(*command_line.get_arguments())
