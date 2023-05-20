from os import listdir
import os.path as p
import argparse
import re
import ast


class LinesChecker:
    def __init__(self, filepath, lines):
        self.path = filepath
        self.lines = lines
        self.MAX_LENGTH = 79
        self.INDENTATION = 4
        self.MAX_SPACES = 2
        self.MAX_EMPTY_LINES = 2
        self.SNAKE_CASE_PATTERN = '^_{0,2}[a-z]([a-z0-9_]*)*$'
        self.CAMEL_CASE_PATTERN = '^[A-Z]([a-z0-9]+[A-Z0-9]*)*$'
        self.ERROR_TEXTS = {'S001': f'Line is longer than {self.MAX_LENGTH} characters',
                            'S002': f'Indentation is not a multiple of {self.INDENTATION}',
                            'S003': 'Unnecessary semicolon after a statement',
                            'S004': f'Less than {self.MAX_SPACES} spaces before inline comment',
                            'S005': 'TODO found',
                            'S006': f'More than {self.MAX_EMPTY_LINES} blank lines preceding a code line',
                            'S007': 'Too many spaces after \'class\' or \'def\'',
                            'S008': 'Class name should use CamelCase',
                            'S009': 'Function name should use snake_case',
                            'S010': 'Argument name should be written in snake_case',
                            'S011': 'Variable should be written in snake_case',
                            'S012': 'The default argument value is mutable'
                            }
        self.check_everything()

    def check_everything(self):
        empty_lines = 0
        for i in range(len(self.lines)):
            line = self.lines[i]
            if not line.strip():
                empty_lines += 1
                continue
            if not self.length_ok(line):
                self.print_error(i + 1, 'S001')
            if not self.indentation_ok(line):
                self.print_error(i + 1, 'S002')
            if not self.semicolon_ok(line):
                self.print_error(i + 1, 'S003')
            if not self.spaces_before_comment_ok(line):
                self.print_error(i + 1, 'S004')
            if self.todo_found(line):
                self.print_error(i + 1, 'S005')
            if empty_lines > self.MAX_EMPTY_LINES:
                self.print_error(i + 1, 'S006')
            empty_lines = 0
            if not self.declaration_ok(line):
                self.print_error(i + 1, 'S007')
            if not self.class_name_ok(line):
                self.print_error(i + 1, 'S008')
            if not self.function_name_ok(line):
                self.print_error(i + 1, 'S009')
            if not self.argument_name_ok(line):
                self.print_error(i + 1, 'S010')
            if not self.variable_name_ok(line):
                self.print_error(i + 1, 'S011')
            if not self.default_argument_ok(line):
                self.print_error(i + 1, 'S012')

    def print_error(self, line, code):
        print(f"{self.path}: Line {line}: {code} - {self.ERROR_TEXTS[code]}.")

    def length_ok(self, line):
        if len(line) > self.MAX_LENGTH:
            return False
        return True

    def indentation_ok(self, line):
        spaces = 0
        if line.startswith(' '):
            for char in line:
                if char != ' ':
                    break
                spaces += 1
            if spaces % self.INDENTATION != 0:
                return False
        return True

    def semicolon_ok(self, line):
        where = line.find('#')
        if where != -1:
            no_comment = line[:where].strip()
            if no_comment.endswith(';'):
                return False
        elif line.strip().endswith(';'):
            return False
        return True

    def spaces_before_comment_ok(self, line):
        where = line.find('#')
        if where > self.MAX_SPACES:
            for i in range(1, self.MAX_SPACES + 1):
                if line[where - i] != ' ':
                    return False
        return True

    def todo_found(self, line):
        where = line.upper().find('TODO')
        if where != -1:
            if line.find('#') != -1 and where > line.find('#'):
                return True
        return False

    def declaration_ok(self, line):
        line = line.strip()
        if line.startswith('class') or line.startswith('def'):
            if line.startswith('class'):
                line = line[5:]
            else:
                line = line[3:]
            if line[0] == ' ' and line[1] == ' ':
                return False
        return True

    def class_name_ok(self, line):
        if line.strip() == '@staticmethod':
            return True
        try:
            tree = ast.parse(line.strip())
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    if not re.match(self.CAMEL_CASE_PATTERN, node.name):
                        return False
            return True
        except IndentationError:
            line = line + '    pass'
            return self.class_name_ok(line)

    def function_name_ok(self, line):
        if line.strip() == '@staticmethod':
            return True
        try:
            tree = ast.parse(line.strip())
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if not re.match(self.SNAKE_CASE_PATTERN, node.name):
                        return False
            return True
        except IndentationError:
            line = line + '    pass'
            return self.function_name_ok(line)

    def argument_name_ok(self, line):
        if line.strip() == '@staticmethod':
            return True
        try:
            tree = ast.parse(line.strip())
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    args = node.args.args
                    for arg in args:
                        if not re.match(self.SNAKE_CASE_PATTERN, arg.arg):
                            return False
            return True
        except IndentationError:
            line = line + '    pass'
            return self.argument_name_ok(line)

    def variable_name_ok(self, line):
        if line.strip() == '@staticmethod':
            return True
        try:
            tree = ast.parse(line.strip())
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    name = node.targets[0]
                    if isinstance(name, ast.Attribute):
                        name = name.attr
                    else:
                        name = name.id
                    if not re.match(self.SNAKE_CASE_PATTERN, name):
                        return False
            return True
        except IndentationError:
            line = line + '    pass'
            return self.variable_name_ok(line)

    def default_argument_ok(self, line):
        if line.strip() == '@staticmethod':
            return True
        try:
            tree = ast.parse(line.strip())
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    defaults = node.args.defaults
                    for default in defaults:
                        if isinstance(default, ast.List):
                            return False
                        if isinstance(default, ast.Dict):
                            return False
                        if isinstance(default, ast.Set):
                            return False
            return True
        except IndentationError:
            line = line + '    pass'
            return self.default_argument_ok(line)


class CommandLine:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('dir')
        args = parser.parse_args()
        self.folder = args.dir
        self.start()

    def start(self):
        files = self.get_filenames(self.folder)
        if files:
            for file in files:
                with open(file, 'r') as f:
                    LinesChecker(file, f.readlines())

    @staticmethod
    def get_filenames(folder):
        filename_pattern = '.*_[0-9]+.py$'
        filenames = list()
        if not p.exists(folder):
            print("Invalid file or directory.")
            return False
        if p.isfile(folder):
            filenames.append(folder)
            return filenames
        scan = listdir(folder)
        for filename in scan:
            if re.match(filename_pattern, filename):
                filename = folder + '\\' + filename
                filenames.append(filename)
        if not filenames:
            print("No correct .py files found in the directory.")
            return False
        return filenames


if __name__ == '__main__':
    CommandLine()
