class MainMenu:
    def __init__(self):
        self.valid_commands = ('plain', 'bold', 'italic', 'header', 'link', 'inline-code', 'ordered-list', 'unordered-list', 'new-line', '!help', '!done')
        self.start()

    def start(self):
        while True:
            user = input("Choose a formatter: ").strip()
            if not user:
                continue
            if user not in self.valid_commands:
                print("Unknown formatting type or command")
                continue
            if user in self.valid_commands[:-2]:
                continue
            if user == self.valid_commands[-2]:
                print("Available formatters: plain bold italic header link inline-code ordered-list unordered-list new-line")
                print("Special commands: !help !done")
                continue
            if user == self.valid_commands[-1]:
                exit()

if __name__ == '__main__':
    MainMenu()