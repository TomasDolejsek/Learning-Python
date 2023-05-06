import re


pattern = "^[+-]?([0-9]+|[a-zA-Z]+)([ ]+[+-]+[ ]+[+-]?([0-9]+|[a-zA-Z]+))*$"

name = "-aaa + -4 - 6  ".strip()

print(re.match(pattern, name) is not None)