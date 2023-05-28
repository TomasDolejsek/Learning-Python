class MarkupModule:
    def markup(self, formatter):
        markup_text = ''
        if formatter == 'new-line':
            markup_text = '\n'
        elif formatter == 'header':
            markup = self.ask_more_info(formatter)
            text = input("Text: ")
            markup_text = markup + text + '\n'
        elif formatter == 'link' or formatter in 'unordered-list':
            markup_text = self.ask_more_info(formatter)
        else:
            text = input("Text: ")
            if formatter == 'plain':
                markup_text = text
            elif formatter == 'bold':
                markup_text = '**' + text + '**'
            elif formatter == 'italic':
                markup_text = '*' + text + '*'
            else:
                markup_text = '`' + text + '`'
        return markup_text

    def ask_more_info(self, what):
        markup = ''
        while True:
            if what == 'header':
                level = input("Level: ").strip()
                try:
                    if not 1 <= int(level) <= 6:
                        raise ValueError
                except ValueError:
                    print("The level should be within the range of 1 to 6.")
                    continue
                markup = '#' * int(level) + ' '
                break
            if what in 'unordered-list':
                rows = input("Number of rows: ").strip()
                try:
                    if not 0 < int(rows):
                        raise ValueError
                except ValueError:
                    print("The number of rows should be greater than zero.")
                    continue
                for i in range(int(rows)):
                    rowtext = input(f"Row # {i + 1}: ")
                    if what[:2] == 'un':
                        markup += '*' + rowtext + '\n'
                    else:
                        markup += f"{i + 1}. " + rowtext + '\n'
                break
            if what == 'link':
                label = input("Label: ")
                url = input("URL: ")
                markup = f"[{label}]({url})"
                break
        return markup

class MainMenu:
    def __init__(self):
        self.valid_commands = ('plain', 'bold', 'italic', 'header', 'link', 'inline-code', 'new-line', 'ordered-list', 'unordered-list', '!help', '!done')
        self.start()

    def start(self):
        whole_text = ''
        mm = MarkupModule()
        while True:
            user = input("Choose a formatter: ").strip().lower()
            if not user:
                continue
            if user not in self.valid_commands:
                print("Unknown formatting type or command.")
                continue
            if user in self.valid_commands[:-2]:
                whole_text += mm.markup(user)
                print(whole_text)
                continue
            if user == self.valid_commands[-2]:
                print("Available formatters: plain bold italic header link inline-code new-line ordered-list unordered-list")
                print("Special commands: !help !done")
                continue
            if user == self.valid_commands[-1]:
                file_to_save = open('output.md', 'w')
                file_to_save.write(whole_text)
                file_to_save.close()
                exit()

if __name__ == '__main__':
    MainMenu()