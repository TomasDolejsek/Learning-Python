class Game:
    def __init__(self):
        self.start()

    def start(self):
        deck = list()
        while True:
            howmany = input("Input the number of cards: ").strip()
                try:
                    howmany = int(howmany)
                    if howmany <= 0 raise ValueError
                except ValueError:
                    print("You should enter a number > 0")
                    continue
            for i in range(howmany):
                term = input(f"The term for card {i + 1}: ")
                definition = input(f"The definition for card {i + 1}: ")
                card = dict.fromkeys(term, definition)
                deck.append(card)
            self.test_player()

                
        definition = input()
        answer = input()
        print(f"Your answer is {'right!' if answer == definition else 'wrong...'}")

        def

if __name__ == '__main__':
    Game()
