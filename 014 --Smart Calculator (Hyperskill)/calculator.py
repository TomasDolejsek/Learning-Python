import re


class InvalidExpression(Exception):
    def __init__(self, whats_wrong):
        self.message = whats_wrong
        super().__init__(self.message)


class Calculator:
    def __init__(self):
        self.variables = dict()

    def all_variables_known(self, expression):
        """
        1) Split given expression into a list
        2) Search the list for variables and replace them with their values
        3) Check signs before all variables. If it's '-', negate the value.
        4) If any of the variables hasn't been defined yet, raise InvalidExpression and return False
        5) Otherwise, return the transformed list of expression members
        """
        exp_list = expression.split()
        try:
            for i in range(len(exp_list)):
                exp = exp_list[i]
                if exp[0] == '-' or exp[0] == '+':  # there can be a sign before the variable
                    exp = exp[1:]
                if exp.isalpha():  # variable found
                    if exp in self.variables:
                        if exp_list[i][0] == '-':
                            exp_list[i] = -self.variables[exp]
                        else:
                            exp_list[i] = self.variables[exp]
                    else:
                        raise InvalidExpression("Unknown variable")
        except InvalidExpression as err:
            print(err)
            return False
        return exp_list

    def calculate(self, expression, *variable):
        """
        1) Check if all variables have been defined
        2) Compute the equation
        3) If there's a variable for assigning, do so.
        4) If not, print the result
        """
        exp_list = self.all_variables_known(expression)
        if not exp_list:
            return
        result = int(exp_list[0])
        for i in range(1, len(exp_list) - 1, 2):
            result = self.compute(result, int(exp_list[i + 1]), self.normalize_operator(exp_list[i]))
        if variable:
            self.variables[variable[0]] = result
        else:
            print(result)

    def compute(self, num1, num2, operation):
        return num1 - num2 if operation == '-' else num1 + num2

    def normalize_operator(self, operator):
        return '-' if operator.count('-') % 2 == 1 else '+'


class ExpressionValidator:
    def __init__(self):
        self.valid_identifier_pattern = "^[a-zA-Z]+[a-zA-Z]*$"
        self.valid_expression_pattern = "^[+-]?([0-9]+|[a-zA-Z]+)([ ]+[+-]+[ ]+[+-]?([0-9]+|[a-zA-Z]+))*$"

    def process_expression(self, exp):
        """
        1) Determine whether given expression is an assignment or not (look for '=')
        2) Send data for validation
        """
        if '=' in exp:
            self.validate_and_assign(exp)
        else:
            self.validate_and_calculate(exp)

    def validate_and_assign(self, exp):
        expression = exp.split('=')
        try:
            if len(expression) > 2:  # too many '=' -> invalid assignment
                raise InvalidExpression('Invalid assignment')
            identifier = expression[0].strip()
            assignment = expression[1].strip()
            if not re.match(self.valid_expression_pattern, assignment):
                raise InvalidExpression('Invalid assignment')
            if not re.match(self.valid_identifier_pattern, identifier):
                raise InvalidExpression('Invalid identifier')
        except InvalidExpression as err:
            print(err)
            return
        calculator.calculate(assignment, identifier)

    def validate_and_calculate(self, exp):
        try:
            if not re.match(self.valid_expression_pattern, exp):
                raise InvalidExpression('Invalid expression')
        except InvalidExpression as err:
            print(err)
            return False
        calculator.calculate(exp)


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
                    print("Smart calculator. Usage: put + or - among numbers.",
                          "You can also assign variables (e.g. a = 3, b = a + 4, etc.)")
                    continue
                if user == '/exit':
                    print("Bye!")
                    exit()
            else:
                validator.process_expression(user)
                continue


if __name__ == '__main__':
    validator = ExpressionValidator()
    calculator = Calculator()
    UserInterface()
