import argparse
import random
import time
import os
from datetime import datetime
import json


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
        loc_name = random.choice(self.possible_locations)
        titanium = random.randint(10, 100)
        locations = {'1': [loc_name, titanium]}
        print("Searching", end='')
        self.animate()
        while True:
            nlocations = len(locations)
            for key, value in locations.items():
                print(f"[{key}] {value[0]}")
            print("\n[S] to continue searching")
            command = self.get_command([*list(locations.keys()), 's', 'back'])
            if command == 's':
                if nlocations < max_locations:
                    loc = random.choice(self.possible_locations)
                    titanium = random.randint(10, 100)
                    locations[str(nlocations + 1)] = [loc, titanium]
                    print("Searching", end='')
                    self.animate()
                else:
                    print("Nothing more in sight.")
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
        self.player = 'player 1'
        self.nrobots = 3
        self.game = Game(args)

    def new_game(self):
        menu = ['[Yes]', '[No]', 'Return to Main[Menu]']
        print(f"\nGreetings, commander {self.player}!")
        while True:
            print('Are you ready to begin?')
            print(*menu, sep=' ')
            command = self.get_command(['yes', 'no', 'menu'])
            if command == 'yes':
                self.play()
                return
            if command == 'no':
                print("\nHow about now.")
                continue
            if command == 'menu':
                return

    def play(self):
        while True:
            self.display()
            command = self.get_command(['ex', 'up', 'save', 'm'])
            if command == 'ex':
                self.score += self.game.explore()
                continue
            if command == 'save':
                self.save()
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

    def save_load_menu(self):
        menu = {'1': 'empty', '2': 'empty', '3': 'empty'}
        for i, data in enumerate(self.get_savegames()):
            if data:
                menu[str(i + 1)] = data
        print("Select save slot:")
        for key, data in menu.items():
            if data == 'empty':
                print(f"[{key}] {data}")
            else:
                print(f"[{key}] {data['Player']} Titanium: {data['Titanium']} Robots: {data['Robots']} Last save: {data['Last_save']}")
        return self.get_command([*menu.keys(), 'back'])

    def save(self):
        data_to_save = {'Player': self.player, 'Titanium': self.score, 'Robots': self.nrobots}
        command = self.save_load_menu()
        if command == 'back':
            return
        now = datetime.now()
        date_time_str = now.strftime("%Y-%m-%d %H:%M")
        data_to_save['Last_save'] = date_time_str
        with open('save_file' + command, 'w') as file:
            json.dump(data_to_save, file)

    def get_savegames(self):
        data_list = list()
        scan = os.listdir()
        for filename in scan:
            if os.path.isfile(filename) and filename.startswith('save_file'):
                with open(filename, 'r') as file:
                    data_list.append(json.load(file))
        return data_list

    def load(self):
        border = '                      |==============================|'
        command = self.save_load_menu()
        if command == 'back':
            return
        with open('save_file' + command, 'r') as file:
            hub_data = json.load(file)
        self.player = hub_data['Player']
        self.score = hub_data['Titanium']
        self.nrobots = hub_data['Robots']
        print(border)
        print('                     |    GAME LOADED SUCCESSFULLY  |')
        print(border)
        print(f"Welcome back, commander {self.player}")


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
        self.menu = ('[New] Game', '[Load] Game', '[High] Scores', '[Help]', '[Exit]')
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
            command = self.get_command(['new', 'load', 'high', 'help', 'exit'])
            if command == 'new':
                print("\nEnter your name:")
                name = input().strip()
                hub.player = name
                hub.new_game()
                continue
            if command == 'load':
                hub.load()
                hub.play()
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
