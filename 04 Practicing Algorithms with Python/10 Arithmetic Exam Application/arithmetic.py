import random


class Calculator:
    @staticmethod
    def calculate(a, b, operator):
        if operator == '-':
            return a - b
        if operator == '+':
            return a + b
        if operator == '*':
            return a * b
        if operator == '^':
            return a ** b


class UserInterface:
    def __init__(self):
        self.valid_operators = ('-', '+', '*', '^')
        self.filename = 'results.txt'
        self.level_descriptions = ('simple operations with numbers 2-9', 'integral squares of 11-29')
        self.start()

    def start(self):
        while True:
            print("1 - ", self.level_descriptions[0])
            print("2 - ", self.level_descriptions[1])
            try:
                level = int(input().strip())
                if not (1 <= level <= 2):
                    raise ValueError
            except ValueError:
                print('Incorrect format.')
                continue
            break
        counter = 0
        correct = 0
        while True:
            if counter == 5:
                break
            if level == 1:
                a = random.randint(2, 9)
                b = random.randint(2, 9)
                operator = random.choice(self.valid_operators[:2])
            else:
                a = random.randint(11, 29)
                b = 2
                operator = self.valid_operators[-1]
            while True:
                if level == 1:
                    print(f"{a} {operator} {b}")
                else:
                    print(a)
                try:
                    user = int(input().strip())
                except ValueError:
                    print("Incorrect format.")
                    continue
                break
            counter += 1
            if user == Calculator.calculate(a, b, operator):
                print("Right!")
                correct += 1
            else:
                print("Wrong!")
        print(f"Your mark is {correct}/5. Would you like to save the result? Enter yes or no.")
        save = input().lower().strip()
        if save == 'yes' or save == 'y':
            self.save_result(correct, level)

    def save_result(self, correct, level):
        print("What is your name?")
        name = input()
        with open(self.filename, 'at') as file:
            file.write(f"{name}: {correct}/5 in level {level} ({self.level_descriptions[level-1]}).\n")
        print(f"The results are saved in \"{self.filename}\".")


if __name__ == '__main__':
    UserInterface()
