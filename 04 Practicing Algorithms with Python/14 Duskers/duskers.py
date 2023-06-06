import argparse
import random
import time


class UserInterface:
    def __init__(self):
        pass

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


class Game(UserInterface):
    def __init__(self, args):
        super().__init__()
        self.delay = random.randint(args.min_anim, args.max_anim)
        random.seed(args.seed)
        self.possible_locations = args.locations.split(',')

    def explore(self):
        max_locations = random.randint(1, 9)
        locations = dict()
        command = 's'
        while True:
            nlocations = len(locations)
            if command == 's':
                if nlocations < max_locations:
                    loc = random.choice(self.possible_locations)
                    titanium = random.randint(10, 100)
                    locations[str(nlocations + 1)] = [loc, titanium]
                    print("Searching", end='')
                    self.animate()
                else:
                    print("Nothing more in sight.")
                for key, value in locations.items():
                    print(f"[{key}] {value[0]}")
                print("\n[S] to continue searching")
                command = self.get_command([*list(locations.keys()), 's', 'back'])
                continue
            if command == 'back':
                return 0
            else:
                return self.deploy(locations[command])

    def animate(self):
        if self.delay != 0:
            for second in range(self.delay + 1):
                time.sleep(1)
                print('.', end='')
        print()

    def deploy(self, location):
        print("Deploying robots", end='')
        self.animate()
        print("Landing", end='')
        self.animate()
        print("Exploring", end='')
        self.animate()
        print(f"{location[0]} explored successfully, with no damage taken.")
        print(f"Acquired {location[1]} lumps of titanium.")
        return location[1]


class Hub(UserInterface):
    def __init__(self, args):
        super().__init__()
        self.ROBOT = ("           __             ",
                      "   _(\    [@@]            ",
                      "  (__/\__ \--/ __         ",
                      "     \___/----\  \   __   ",
                      "         \ }{ /\  \_/ _\  ",
                      "         /\__/\ \__O (__  ",
                      "        (--/\--)    \__/  ",
                      "        _)(  )(_          ",
                      "       `---''---`         ")
        self.score = 0
        self.game = Game(args)

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
                    if command == 'ex':
                        self.score += self.game.explore()
                        continue
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
        print(f"| Titanium: {self.score}{' ' * (68 - len(str(self.score)))}|")
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


class MainMenu(UserInterface):
    def __init__(self):
        super().__init__()
        self.LOGO = ("═════════════════════════════════════════════════════════",
                     "██████╗░██╗░░░██╗░██████╗██╗░░██╗███████╗██████╗░░██████╗",
                     "██╔══██╗██║░░░██║██╔════╝██║░██╔╝██╔════╝██╔══██╗██╔════╝",
                     "██║░░██║██║░░░██║╚█████╗░█████═╝░█████╗░░██████╔╝╚█████╗░",
                     "██║░░██║██║░░░██║░╚═══██╗██╔═██╗░██╔══╝░░██╔══██╗░╚═══██╗",
                     "██████╔╝╚██████╔╝██████╔╝██║░╚██╗███████╗██║░░██║██████╔╝",
                     "╚═════╝░░╚═════╝░╚═════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝╚═════╝░",
                     "             (Survival ASCII Strategy Game)              ")
        self.menu = ('[Play]', '[High] Scores', '[Help]', '[Exit]')
        self.args = self.get_arguments()
        self.start()

    def get_arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('seed', default=0)
        parser.add_argument('min_anim', type=int, default=0)
        parser.add_argument('max_anim', type=int, default=0)
        parser.add_argument('locations', default='')
        return parser.parse_args()

    def start(self):
        hub = Hub(self.args)
        while True:
            print(*self.LOGO, sep='\n')
            print(*self.menu, sep='\n')
            command = self.get_command(['play', 'high', 'help', 'exit'])
            if command == 'play':
                print("\nEnter your name:")
                name = input().strip()
                hub.play(name)
                continue
            if command == 'high':
                hub.high_score()
                continue
            if command == 'help':
                hub.help()
                continue
            if command == 'exit':
                print("Thanks for playing, bye!")
                exit()


if __name__ == '__main__':
    MainMenu()
