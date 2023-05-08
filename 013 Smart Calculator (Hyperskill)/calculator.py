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
        2) If any of the variables hasn't been defined yet, return False.
        3) Otherwise, return the transformed list of expression members.
        """
        for i in range(len(exp_list)):
            multiplier = 1
            member = exp_list[i]
            if len(member) > 1:
                if member[0] == '-' or member[0] == '+':
                    if member[0] == '-':
                        multiplier = -1
                    member = member[1:]
            *alphas, = map(lambda x: x.isalpha(), member)
            if any(alphas):
                if member in self.variables:
                    exp_list[i] = str(int(self.variables[member]) * multiplier)
                else:
                    return False
        return exp_list

    def transform_to_postfix(self, exp_list):
        """
        1) Convert given list of expression members to postfix notation for easier calculation.
        """
        postfix = deque()
        stack = deque()
        for member in exp_list:
            try:
                int(member)
                postfix.append(member)
                continue
            except ValueError:
                pass
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

    def calculate(self, exp_list, *variable):
        """
        1) Replace variables among the expression members with their values.
        2) Convert the expression members list to postfix notation for easier calculation.
        3) Compute the result.
        4) If there's a variable for assigning to, do so. If not, print the result.
        """
        try:
            exp_list = self.all_variables_known(exp_list)
            if not exp_list:
                raise InvalidEquation('Unknown variable')
        except InvalidEquation as err:
            print(err)
            return
        postfix = self.transform_to_postfix(exp_list)
        stack = deque()
        for member in postfix:
            try:
                int(member)
                stack.append(member)
                continue
            except ValueError:
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


class EquationValidator:
    def __init__(self):
        self.valid_identifier_pattern = "^[a-zA-Z]+[a-zA-Z]*$"
        self.valid_expression_pattern = "^[+-]*([0-9]+|[a-zA-Z]+)(([+-]+|[*/^]?)([+-]*)?([0-9]+|[a-zA-Z]+))*$"
        self.supported_operators = ('-', '+', '*', '/', '^')

    def process_equation(self, equation):
        """
        1) Separate given equation into left side (before '=') and right side (after '=').
           Note: Separate only by the first appearance of '='.
        2) Validate both sides of the equation (if there is only one side, then it's an expression).
        3) If validity is confirmed, separate the expression into list of expression members.
        4) Send the list to the calculator.
        """
        separated = equation.split('=', 1)
        try:
            if len(separated) > 1:
                identifier = separated[0]
                assignment = separated[1]
                validmsg = self.validate(assignment, identifier)
                if validmsg is not True:
                    raise InvalidEquation(validmsg)
                exp_list = self.separate_expression_members(assignment)
                calculator.calculate(exp_list, identifier)
                return
            else:
                expression = separated[0]
                validmsg = self.validate(expression)
                if validmsg is not True:
                    raise InvalidEquation(validmsg)
                exp_list = self.separate_expression_members(expression)
                calculator.calculate(exp_list)
                return
        except InvalidEquation as err:
            print(err)
            return

    def validate(self, exp, *ident):
        """
        1) For testing purposes, create temporary expression without parentheses.
           During the process check if amount of left and right parentheses is equal and correctly distributed.
           Return an error message if there is such a problem.
        2) Compare the temporary expression (and identifier if it's also given) with the valid patterns.
           Again, return an error message if there is no match.
        3) Return True if both checks were successful.
        """
        paren = 0  # number of parentheses; '(' = +1 ')' = -1. This number can go below 0 and must = 0 in total
        check_exp = ''
        for i in range(len(exp)):
            char = exp[i]
            if char == '(':
                paren += 1
            elif char == ')':
                paren -= 1

                # Check if there isn't operator right before ')' which is wrong.
                if exp[i-1] in self.supported_operators:
                    return 'Invalid assignment' if ident else 'Invalid expression'

            # Check if there aren't mixed operators.
            # There can be only '-' and '+' more than one next to each other.
            elif char in self.supported_operators:
                if char == '+' or char == '-':
                    if exp[i-1] == '*' or exp[i-1] == '/' or exp[i-1] == '^':
                        return 'Invalid assignment' if ident else 'Invalid expression'
                else:
                    if exp[i-1] in self.supported_operators:
                        return 'Invalid assignment' if ident else 'Invalid expression'
                check_exp += char
            else:
                check_exp += char
            if paren < 0:
                return 'Invalid assignment' if ident else 'Invalid expression'
        if paren != 0:
            return 'Invalid assignment' if ident else 'Invalid expression'

        # Check the patterns (without parentheses).
        if ident:
            if not re.match(self.valid_identifier_pattern, ident[0]):
                return 'Invalid identifier'
            if not re.match(self.valid_expression_pattern, check_exp):
                return 'Invalid assignment'
        else:
            if not re.match(self.valid_expression_pattern, check_exp):
                return 'Invalid expression'
        return True

    def separate_expression_members(self, expression):
        """
        1) Add '0+' to the beginning of given expression to avoid problems with '-' or '+' starting the expression.
           Also add ' ' to the end of the expression to be always within index range during the separation process
           and to mark end of the expression.
        2) Go through the expression letter by letter and find logical patterns
           (aka letters, numbers, operators and parentheses).
        3) Replace all multiple '-' and '+' to single operator (e.g. 3+--6 => 3+6).
        4) Be sure to distinct between signs and operators.
           e.g. 3-6 => '-' is an operator whereas in -3+6 '-' is a sign.
           Be sure to add all operands into the list of expression members with correct signs.
        5) Next, replace all signs right behind parentheses with -1* or 1* (e.g. -(-6)) => -(-1*6). This is the only way
           to make postfix calculation work correctly.
        6) Separate these units into the list of expression members and return the list.
        """
        members = list()
        i = 0
        expression = '0+' + expression + ' '
        while True:
            member = ''
            if expression[i] == ' ':
                break
            if expression[i] == '(':
                members.append(expression[i])
                i += 1
                mark = i
                if expression[i] == '-' or expression[i] == '+':
                    member = ''
                    while expression[i] == '-' or expression[i] == '+':
                        member += expression[i]
                        i += 1
                    op = self.normalize_operator(member)
                    stepback = len(member)
                    member = ''
                    if expression[i] == '(':
                        expression = expression[:mark] + op + '1*' + expression[mark + stepback:]
                        members.pop()
                        i = mark - 1
                        continue
                    while expression[i].isalpha() or expression[i].isnumeric():
                        member += expression[i]
                        i += 1
                    if op == '-':
                        member = '-' + member
                    members.append(member)
                    continue
            if expression[i] == ')':
                members.append(expression[i])
                i += 1
                continue
            if expression[i] in self.supported_operators:
                while expression[i] in self.supported_operators:
                    member += expression[i]
                    i += 1
                members.append(self.normalize_operator(member))
                continue
            while expression[i].isalpha() or expression[i].isnumeric():  # this is why we need extra ' '
                member += expression[i]
                i += 1
            members.append(member)
        return members

    def normalize_operator(self, operator):
        if '-' in operator or '+' in operator:
            if operator.count('-') % 2 == 1:
                return '-'
            else:
                return '+'
        else:
            return operator


class UserInterface:
    def __init__(self):
        self.valid_commands = ('/help', '/exit')
        self.start()

    def start(self):
        while True:
            user = input().replace(' ', '')
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
