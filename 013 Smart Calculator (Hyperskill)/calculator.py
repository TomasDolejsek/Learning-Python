import re
from collections import deque


class InvalidEquation(Exception):
    def __init__(self, whats_wrong):
        self.message = whats_wrong
        super().__init__(self.message)


class Calculator:
    def __init__(self):
        self.variables = dict()
        self.op_priorities = {'-': 1, '+': 1, '*': 2, '/': 2, '^': 3}

    def all_variables_known(self, exp_list):
        """
        1) Search given list of expression members for variables and replace them with their values.
        2) If any of the variables hasn't been defined yet, raise InvalidEquation and return False.
        3) Otherwise, return the transformed list of expression members.
        """
        try:
            for i in range(len(exp_list)):
                exp = exp_list[i]
                *alphas, = map(lambda x: x.isalpha(), exp)
                if any(alphas):  # variable found
                    if exp in self.variables:
                        exp_list[i] = self.variables[exp]
                    else:
                        raise InvalidEquation("Unknown variable")
        except InvalidEquation as err:
            print(err)
            return False
        return exp_list

    def separate_expression_members(self, expression):
        """
        1) Go through the expression letter by letter and find logical patterns
           (aka letters, numbers, operators etc.).
        2) Separate these units into the list of expression members.
        3) Return the list.
        """
        members = list()
        i = 0
        expression += ' '  # adding extra ' ' to be always in index range
        while i < len(expression):
            member = ''
            if expression[i] == ' ':
                i += 1
                continue
            elif expression[i] == '(' or expression[i] == ')':
                members.append(expression[i])
                i += 1
                continue
            elif expression[i] in self.op_priorities:
                while expression[i] in self.op_priorities:
                    member += expression[i]
                    i += 1
                members.append(self.normalize_operator(member))
                continue
            while expression[i].isalpha() or expression[i].isnumeric():  # this is why we need extra ' '
                member += expression[i]
                i += 1
            members.append(member)
        return members

    def transform_to_postfix(self, exp_list):
        """
        1) Convert given expression to postfix notation for easier calculation
        """
        postfix = deque()
        stack = deque()
        for member in exp_list:
            if member.isnumeric():
                postfix.append(member)
                continue
            if member in self.op_priorities:
                if len(stack) == 0 or stack[-1] == '(':
                    stack.append(member)
                    continue
                if self.op_priorities[member] > self.op_priorities[stack[-1]]:
                    stack.append(member)
                    continue
                if self.op_priorities[member] <= self.op_priorities[stack[-1]]:
                    while True:
                        if not stack:
                            break
                        if stack[-1] == '(':
                            break
                        if self.op_priorities[member] > self.op_priorities[stack[-1]]:
                            break
                        poped = stack.pop()
                        postfix.append(poped)
                    stack.append(member)
                    continue
            if member == '(':
                stack.append(member)
                continue
            if member == ')':
                while True:
                    poped = stack.pop()
                    if poped == '(':
                        break
                    postfix.append(poped)
                continue
        for _ in range(len(stack)):
            postfix.append(stack.pop())
        return postfix

    def calculate(self, expression, *variable):
        """
        1) Separate given expression into expression members.
        2) Replace variables among the expression members with their values.
        3) Convert the expression members list to postfix notation for easier calculation
        4) Compute the result.
        5) If there's a variable for assigning to, do so. If not, print the result.
        """
        exp_list = self.separate_expression_members(expression)
        exp_list = self.all_variables_known(exp_list)
        if not exp_list:  # undefined variable found, can't calculate
            return
        postfix = self.transform_to_postfix(exp_list)
        stack = deque()

        for member in postfix:
            if member.isnumeric():
                stack.append(member)
                continue
            if member in self.op_priorities:
                n1 = stack.pop()
                n2 = stack.pop()
                result = self.compute(int(n2), int(n1), member)
                stack.append(result)

        if variable:
            self.variables[variable[0]] = str(stack[-1])
        else:
            print(stack[-1])

    def compute(self, num1, num2, operator):
        if operator == '-':
            return num1 - num2
        elif operator == '+':
            return num1 + num2
        elif operator == '*':
            return num1 * num2
        elif operator == '/':
            return num1 // num2
        else:
            return num1 ** num2

    def normalize_operator(self, operator):
        if '-' in operator or '+' in operator:
            if operator.count('-') % 2 == 1:
                return '-'
            else:
                return '+'
        else:
            return operator


class EquationValidator:
    def __init__(self):
        self.valid_identifier_pattern = "^[a-zA-Z]+[a-zA-Z]*$"
        self.valid_expression_pattern = "^[+-]?([0-9]+|[a-zA-Z]+)([ ]*([+-]+|[*/^]?)([ ]*[+-]*)?([0-9]+|[a-zA-Z]+))*$"

    def process_equation(self, equation):
        """
        1) Separate given equation into left side (before '=') and right side (after '=').
           Note: Separate only by the first appearance of '='.
        2) Validate both sides of the equation (if there is only one side, then it's an expression).
        3) If validity is confirmed, send the equation (or the expression) to the calculator.
        """
        separated = equation.split('=', 1)
        if len(separated) > 1:
            identifier = separated[0].strip()
            assignment = separated[1].strip()
            if self.validate(assignment, identifier):
                calculator.calculate(assignment, identifier)
            else:
                return
        else:
            expression = separated[0].strip()
            if self.validate(expression):
                calculator.calculate(expression)
            else:
                return

    def validate(self, exp, *ident):
        """
        1) For testing purposes, create temporary expression without parentheses.
           During the process check if amount of left and right parentheses is equal and correctly distributed.
           Raise InvalidEquation if there is such problem.
        2) Compare the temporary expression (and identifier if it's also given) with the valid patterns.
           Raise InvalidEquation if there is no match.
        3) Return the result (True = validated, False = not validated)
        """
        try:
            paren = 0
            check_exp = ''
            for char in exp:
                if char == '(':
                    paren += 1
                elif char == ')':
                    paren -= 1
                else:
                    check_exp += char
                if paren < 0:  # there can never be more right parentheses than the left ones.
                    raise InvalidEquation('Invalid expression')
            if paren != 0:
                raise InvalidEquation('Invalid expression')
            if ident:
                if not re.match(self.valid_identifier_pattern, ident[0]):
                    raise InvalidEquation('Invalid identifier')
                if not re.match(self.valid_expression_pattern, check_exp):
                    raise InvalidEquation('Invalid assignment')
            else:
                if not re.match(self.valid_expression_pattern, check_exp):
                    raise InvalidEquation('Invalid expression')
        except InvalidEquation as err:
            print(err)
            return False
        return True


class UserInterface:
    def __init__(self):
        self.valid_commands = ('/help', '/exit')
        self.start()

    def start(self):
        while True:
            user = input().strip()
            if len(user) == 0:  # empty or none input
                continue
            if user[0] == '/':  # input is a command, not expression
                if user not in self.valid_commands:
                    print("Unknown command")
                    continue
                if user == '/help':
                    print("Smart calculator. Usage: put operators among numbers.",
                          "Supported operators are: -  +  *  /  ^",
                          "You can also assign variables and use parentheses.", sep='\n')
                    continue
                if user == '/exit':
                    print("Bye!")
                    exit()
            validator.process_equation(user)


if __name__ == '__main__':
    validator = EquationValidator()
    calculator = Calculator()
    UserInterface()
