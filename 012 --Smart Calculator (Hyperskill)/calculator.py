import re
def compute(num1, num2, operation):
    return num1 - num2 if operation == '-' else num1 + num2

def normalize_operator(operator):
    return '-' if operator.count('-') % 2 == 1 else '+'

def is_valid_expression(inp):
    if len(inp.strip()) == 0:  # empty or none input
        return False
    if inp[0] == '/':  # input is a command, not expression
        if inp not in valid_commands:
            print("Unknown command")
            return False
        if inp == '/help':
            print("Smart calculator. Usage: put + or - among numbers.")
            return False
        if inp == '/exit':
            print("Bye!")
            exit()

    if re.match(valid_input_pattern, inp) is None:  # incorrect expression
        print("Invalid expression")
        return False
    return True

# main program
valid_input_pattern = "^[+-]?[0-9]+([ ]+[+-]+[ ]+[+-]?[0-9]+)*$"
valid_commands = ['/help','/exit']
def start():
    while True:
        user_input = input()
        if not is_valid_expression(user_input):
            continue
        members = user_input.split()  # splitting input into a list of expression members
        result = int(members[0])
        for i in range(1, len(members) - 1, 2):
            result = compute(result, int(members[i + 1]), normalize_operator(members[i]))
        print(result)

# Program must be executed as main, otherwise it does nothing (for testing purposes).
if __name__ == '__main__':
    start()