class Duskers:
    def __init__(self):
        self.ROBOT = ("           __             ",
                      "   _(\    [@@]            ",
                      "  (__/\__ \--/ __         ",
                      "     \___/----\  \   __   ",
                      "         \ }{ /\  \_/ _\  ",
                      "         /\__/\ \__O (__  ",
                      "        (--/\--)    \__/  ",
                      "        _)(  )(_          ",
                      "       `---''---`         ")

    @staticmethod
    def get_command(options):
        while True:
            print("\nYour command:")
            command = input().lower().strip()
            if command not in options:
                print("Invalid input")
                continue
            break
        return command

    def play(self, name):
        menu = ['[Yes]', '[No]', 'Return to Main[Menu]']
        print(f"\nGreetings, commander {name}!")
        while True:
            print('Are you ready to begin?')
            print(*menu, sep=' ')
            command = self.get_command(['yes', 'no', 'menu'])
            if command == 'yes':
                while True:
                    self.display()
                    command = self.get_command(['ex', 'up', 'save', 'm'])
                    if command == 'm':
                        answer = self.game_menu()
                        if answer == 'back':
                            continue
                        if answer == 'main':
                            return
                        if answer == 'save':
                            self.save()
                            continue
                        else:
                            print("Thanks for playing, bye!")
                            exit()
                    else:
                        print("Coming SOON! Thanks for playing!")
                        exit()
            if command == 'no':
                print("\nHow about now.")
                continue
            if command == 'menu':
                return

    def display(self):
        border = "+===============================================================================+"
        menu = ("|                  [Ex]plore                          [Up]grade                 |",
                "|                  [Save]                             [M]enu                    |")
        print(border)
        for line in self.ROBOT:
            print(f"{line}|{line}|{line}")
        print(border)
        print(*menu, sep='\n')
        print(border)

    def game_menu(self):
        border = "                  |==========================|"
        menu = ("                  |            MENU          |",
                "                  |                          |",
                "                  | [Back] to game           |",
                "                  | Return to [Main] Menu    |",
                "                  | [Save] and exit          |",
                "                  | [Exit] game              |")
        print(border)
        print(*menu, sep='\n')
        print(border)
        return self.get_command(['back', 'main', 'save', 'exit'])

    def high_score(self):
        menu = ['[Back]']
        print("No scores to display")
        print(*menu, sep=' ')
        command = self.get_command(['back'])
        if command == 'back':
            return

    @staticmethod
    def help():
        print("Coming SOON! Thanks for playing!")
        exit()

    @staticmethod
    def save():
        print("Coming SOON! Thanks for playing!")
        exit()

class MainMenu:
    def __init__(self):
        self.LOGO = ("═════════════════════════════════════════════════════════",
                     "██████╗░██╗░░░██╗░██████╗██╗░░██╗███████╗██████╗░░██████╗",
                     "██╔══██╗██║░░░██║██╔════╝██║░██╔╝██╔════╝██╔══██╗██╔════╝",
                     "██║░░██║██║░░░██║╚█████╗░█████═╝░█████╗░░██████╔╝╚█████╗░",
                     "██║░░██║██║░░░██║░╚═══██╗██╔═██╗░██╔══╝░░██╔══██╗░╚═══██╗",
                     "██████╔╝╚██████╔╝██████╔╝██║░╚██╗███████╗██║░░██║██████╔╝",
                     "╚═════╝░░╚═════╝░╚═════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝╚═════╝░",
                     "             (Survival ASCII Strategy Game)              ")
        self.menu = ('[Play]', '[High] Scores', '[Help]', '[Exit]')
        self.start()

    def start(self):
        while True:
            print(*self.LOGO, sep='\n')
            print(*self.menu, sep='\n')
            command = game.get_command(['play', 'high', 'help', 'exit'])
            if command == 'play':
                print("\nEnter your name:")
                name = input().strip()
                game.play(name)
                continue
            if command == 'high':
                game.high_score()
                continue
            if command == 'help':
                game.help()
                continue
            if command == 'exit':
                print("Thanks for playing, bye!")
                exit()


if __name__ == '__main__':
    game = Duskers()
    MainMenu()
