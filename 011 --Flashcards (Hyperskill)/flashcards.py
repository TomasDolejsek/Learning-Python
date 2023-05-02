class Flashcards:
    def __init__(self):
        self.deck = dict()
        self.start()

    def start(self):
        self.build_deck()
        self.test_player()
        exit()

    def build_deck(self):
        while True:
            howmany = input("Input the number of cards:\n")
            try:
                if int(howmany) <= 0:
                    raise ValueError
            except ValueError:
                print("You should enter a number > 0")
                continue
            for i in range(int(howmany)):
                print(f"The term for card #{i + 1}:")
                while True:
                    term = input()
                    if term in self.deck.keys():
                        print(f"The term \"{term}\" already exists. Try again:")
                        continue
                    else:
                        break
                print(f"The definition for card #{i + 1}:")
                while True:
                    definition = input()
                    if definition in self.deck.values():
                        print(f"The definition \"{definition}\" already exists. Try again:")
                        continue
                    else:
                        break
                self.deck[term] = definition
            break

    def test_player(self):
        for term, definition in self.deck.items():
            answer = input(f"Print the definition of \"{term}\":\n")
            if answer == definition:
                print("Correct!")
            else:
                print(f"Wrong. The right answer is \"{definition}\"", end='')
                if answer in self.deck.values():
                    searched_key = [k for k, v in self.deck.items() if v == answer]
                    print(f", but your definition is correct for \"{searched_key[0]}\"")
                else:
                    print()


if __name__ == '__main__':
    Flashcards()
