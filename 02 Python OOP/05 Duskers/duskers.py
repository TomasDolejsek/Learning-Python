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
            print("\nYour command: ", end='')
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

    def explore(self, equipment):
        max_locations = random.randint(1, 9)
        locations = dict()
        command = 's'
        while True:
            nlocations = len(locations)
            if command == 's':
                if nlocations < max_locations:
                    loc = random.choice(self.possible_locations)
                    titanium = random.randint(10, 100)
                    encounter = random.random()
                    locations[str(nlocations + 1)] = [loc, titanium, encounter]
                    print("Searching", end='')
                    self.animate()
                    for key, value in locations.items():
                        print(f"[{key}] {value[0]} ", end='')
                        if equipment[1]:
                            print(f"Titanium: {value[1]} ", end='')
                        if equipment[2]:
                            print(f"Encounter rate: {value[2] * 100:.0f}%", end='')
                        print()
                    print("\n[S] to continue searching")
                else:
                    print("Nothing more in sight.")
                print("[Back]")
                command = self.get_command([*list(locations.keys()), 's', 'back'])
                continue
            if command == 'back':
                return 0, False
            else:
                return self.deploy(locations[command], equipment[0])

    def animate(self):
        if self.delay != 0:
            for second in range(self.delay):
                time.sleep(1)
                print('.', end='')
        print()

    def deploy(self, location, nrobots):
        print("Deploying robots", end='')
        self.animate()
        print("Landing", end='')
        self.animate()
        print("Exploring", end='')
        self.animate()
        enemy = random.random()
        lost = False
        if enemy < location[2]:
            lost = True
            print("ENEMY ENCOUNTER!")
            if nrobots == 1:
                print("Mission aborted, the last robot lost...")
                return 0, lost
            print(f"{location[0]} explored successfully, 1 robot lost.")
        else:
            print(f"{location[0]} explored successfully, with no damage taken.")
        print(f"Acquired {location[1]} lumps of titanium.")
        return location[1], lost


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
        self.player = 'player 1'
        self.score = 0
        self.nrobots = 3
        self.titanium_scan = False
        self.enemy_scan = False
        self.game = Game(args)

    def new_game(self, player):
        self.player = player
        self.score = 0
        self.nrobots = 3
        self.titanium_scan = False
        self.enemy_scan = False
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
            equipment = [self.nrobots, self.titanium_scan, self.enemy_scan]
            command = self.get_command(['ex', 'up', 'save', 'm'])
            if command == 'ex':
                gain, lost = self.game.explore(equipment)
                self.score += gain
                if lost:
                    self.nrobots -= 1
                if self.nrobots == 0:
                    print("                        |==============================|")
                    print("                        |          GAME OVER!          |")
                    print("                        |==============================|")
                    self.new_high_score()
                    return
                continue
            if command == 'up':
                self.upgrade()
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
                    print("Thanks for playing, bye!")
                    exit()
                if answer == 'exit':
                    print("Thanks for playing, bye!")
                    exit()

    def display(self):
        border = "+===============================================================================+"
        menu = ("|                  [Ex]plore                          [Up]grade                 |",
                "|                  [Save]                             [M]enu                    |")
        print(border)
        for line in self.ROBOT:
            text = line + ('|' + line) * (self.nrobots - 1)
            print(text)
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

    def upgrade(self):
        prices = {'1': 250, '2': 500, '3': 1000}
        texts = {'1': 'Titanium Scan', '2': 'Enemy Encounter Scan', '3': 'New Robot'}
        print("                     |================================|")
        print("                     |          UPGRADE STORE         |")
        print("                     |                         Price  |")
        print("                     | [1] Titanium Scan         250  |")
        print("                     | [2] Enemy Encounter Scan  500  |")
        print("                     | [3] New Robot            1000  |")
        print("                     |                                |")
        print("                     | [Back]                         |")
        print("                     |================================|")
        while True:
            command = self.get_command(['1', '2', '3', 'back'])
            if command == 'back':
                return
            if prices[command] > self.score:
                print("Not enough titanium!")
                continue
            break
        self.score -= prices[command]
        if command == '1':
            self.titanium_scan = True
        elif command == '2':
            self.enemy_scan = True
        elif command == '3':
            self.nrobots += 1
        print("Purchase successful.", texts[command])

    def display_high_scores(self):
        menu = ['[Back]']
        file_name = 'high_scores'
        if os.path.isfile(file_name):
            print("     HIGH SCORES")
            with open(file_name, 'r') as file:
                high_scores = json.load(file)
            for i, score in enumerate(high_scores):
                print(f"({i + 1}) {score[0]} {score[1]}")
        else:
            print("No scores to display")
        print()
        print(*menu, sep=' ')
        command = self.get_command(['back'])
        if command == 'back':
            return

    def new_high_score(self):
        file_name = 'high_scores'
        high_scores = list()
        if os.path.isfile(file_name):
            with open(file_name, 'r') as file:
                high_scores = json.load(file)
        high_scores.append([self.player, self.score])
        high_scores.sort(key=lambda x: x[1], reverse=True)
        with open(file_name, 'w') as file:
            json.dump(high_scores[:10], file)

    def help(self):
        print("Hyperskill Project.")

    def save_load_menu(self):
        menu = {'1': 'empty', '2': 'empty', '3': 'empty'}
        for data in self.get_savegames():
            if data:
                menu[data['Slot']] = data
        print("\n Select save slot:")
        for slot, item in menu.items():
            if item == 'empty':
                print(f"  [{slot}] {item}")
            else:
                print(f"  [{slot}] {item['Player']} Titanium: {item['Titanium']} ", end='')
                print(f"Robots: {item['Robots']} Last save: {item['Last_save']}")
        print("\n  [Back]")
        return self.get_command([*menu.keys(), 'back'])

    def save(self):
        command = self.save_load_menu()
        if command == 'back':
            return
        data_to_save = {'Slot': command,
                        'Player': self.player,
                        'Titanium': self.score,
                        'Robots': self.nrobots,
                        'Titanium_scan': self.titanium_scan,
                        'Enemy_scan': self.enemy_scan}
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
        while True:
            command = self.save_load_menu()
            if command == 'back':
                return
            if not os.path.exists('save_file' + command):
                print("Empty slot!")
                continue
            break
        with open('save_file' + command, 'r') as file:
            hub_data = json.load(file)
        self.player = hub_data['Player']
        self.score = hub_data['Titanium']
        self.nrobots = hub_data['Robots']
        self.titanium_scan = hub_data['Titanium_scan']
        self.enemy_scan = hub_data['Enemy_scan']
        print(border)
        print('                      |    GAME LOADED SUCCESSFULLY  |')
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
                hub.new_game(name)
                continue
            if command == 'load':
                hub.load()
                hub.play()
                continue
            if command == 'high':
                hub.display_high_scores()
                continue
            if command == 'help':
                hub.help()
                continue
            if command == 'exit':
                print("Thanks for playing, bye!")
                exit()


if __name__ == '__main__':
    MainMenu()
