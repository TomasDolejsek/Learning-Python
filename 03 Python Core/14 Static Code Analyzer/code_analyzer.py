from os import listdir
import os.path as p
import argparse
import re
import ast


class Analyzer:
    def __init__(self, filepath, script):
        self.path = filepath
        self.tree = ast.parse(script)
        self.lines = script.splitlines()
        self.nodes = list()
        self.startlines = list()
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
        self.logger = list()
        self.find_all_nodes(self.tree.body)
        self.check_everything()

    def check_everything(self):
        prevline = 0
        for i, (node, startline) in enumerate(zip(self.nodes, self.startlines)):
            if startline - prevline > self.MAX_EMPTY_LINES + 1:
                self.add_to_logger(startline, 'S006')
            prevline = startline
            if i < len(self.startlines) - 1:
                endline = self.startlines[i + 1] - 1
            else:
                endline = len(self.lines)
            for curline in range(startline, endline + 1):
                line = self.lines[curline - 1]
                if not self.length_ok(line):
                    self.add_to_logger(curline, 'S001')
                if not self.indentation_ok(line):
                    self.add_to_logger(curline, 'S002')
                if not self.semicolon_ok(line):
                    self.add_to_logger(curline, 'S003')
                if not self.spaces_before_comment_ok(line):
                    self.add_to_logger(curline, 'S004')
                if self.todo_found(line):
                    self.add_to_logger(curline, 'S005')
                if not self.declaration_ok(line):
                    self.add_to_logger(curline, 'S007')
            if not self.class_name_ok(node):
                self.add_to_logger(startline, 'S008')
            if not self.function_name_ok(node):
                self.add_to_logger(startline, 'S009')
            if not self.argument_name_ok(node):
                self.add_to_logger(startline, 'S010')
            if not self.variable_name_ok(node):
                self.add_to_logger(startline, 'S011')
            if not self.default_argument_ok(node):
                self.add_to_logger(startline, 'S012')
        self.print_logger()

    def add_to_logger(self, line, code):
        tline = str(line)
        if line < 100:
            tline = '0' + tline
        if line < 10:
            tline = '0' + tline
        self.logger.append(f"{self.path}: Line {tline}: {code} - {self.ERROR_TEXTS[code]}.")

    def print_logger(self):
        self.logger.sort()
        for line in self.logger:
            index = line.find('Line ')
            old_line_text = line[index:index + 8]
            num = str(int(old_line_text[-3:]))
            line = line.replace(old_line_text, 'Line ' + num)
            print(line)

    def find_all_nodes(self, root):
        for node in root:
            self.nodes.append(node)
            self.startlines.append(node.lineno)
            if isinstance(node, ast.ClassDef) or isinstance(node, ast.FunctionDef):
                self.find_all_nodes(node.body)

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

    def class_name_ok(self, node):
        if isinstance(node, ast.ClassDef):
            if not re.match(self.CAMEL_CASE_PATTERN, node.name):
                return False
        return True

    def function_name_ok(self, node):
        if isinstance(node, ast.FunctionDef):
            if not re.match(self.SNAKE_CASE_PATTERN, node.name):
                return False
        return True

    def argument_name_ok(self, node):
        if isinstance(node, ast.FunctionDef):
            args = node.args.args
            for arg in args:
                if not re.match(self.SNAKE_CASE_PATTERN, arg.arg):
                    return False
        return True

    def variable_name_ok(self, node):
        if isinstance(node, ast.Assign):
            variable = node.targets[0]
            if not isinstance(variable, ast.Attribute):
                if not re.match(self.SNAKE_CASE_PATTERN, variable.id):
                    return False
        return True

    def default_argument_ok(self, node):
        if isinstance(node, ast.FunctionDef):
            defaults = node.args.defaults
            for default in defaults:
                if isinstance(default, ast.List) \
                 or isinstance(default, ast.Dict) \
                 or isinstance(default, ast.Set):
                    return False
        return True


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
                    Analyzer(file, f.read())

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
