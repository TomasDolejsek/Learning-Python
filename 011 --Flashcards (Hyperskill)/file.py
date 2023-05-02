class Flashcards:
    def __init__(self):
        self.deck = dict()
        self.start()

    def start(self):
        while True:
            howmany = input("Input the number of cards:\n")
            try:
                howmany = int(howmany)
                if howmany <= 0:
                    raise ValueError
            except ValueError:
                print("You should enter a number > 0")
                continue
            for i in range(howmany):
                term = input(f"The term for card #{i + 1}:\n")
                definition = input(f"The definition for card #{i + 1}:\n")
                self.deck[term] = definition
            self.test_player()
            exit()

    def test_player(self):
        for term, definition in self.deck.items():
            answer = input(f"Print the definition of \"{term}\":\n")
            if answer == definition:
                print("Correct!")
            else:
                print(f"Wrong. The right answer is \"{definition}\"")


if __name__ == '__main__':
    Flashcards()
