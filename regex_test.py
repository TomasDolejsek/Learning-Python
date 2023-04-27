import re

pattern = "^[+-]?[0-9]+([ ]+[+-]+[ ]+[+-]?[0-9]+)*$"

name = "-2"

print(re.match(pattern, name) is not None)