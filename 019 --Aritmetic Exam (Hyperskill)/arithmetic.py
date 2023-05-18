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


class UserInterface:
    def __init__(self):
        self.valid_operators = ('-', '+', '*')
        self.start()

    def start(self):
        a = random.randint(2, 9)
        b = random.randint(2, 9)
        operator = random.choice(self.valid_operators)
        print(f"{a} {operator} {b}")
        user = int(input())
        if user == Calculator.calculate(a, b, operator):
            print("Right!")
        else:
            print("Wrong!")


if __name__ == '__main__':
    UserInterface()
