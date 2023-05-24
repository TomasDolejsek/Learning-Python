import re

#"^[+-]?([0-9]+|[a-zA-Z]+)([ ]*([+-]+|[*/^]?)([ ]*[+-]*)?([0-9]+|[a-zA-Z]+))*$"
#"^[+-]?([0-9]+|[a-zA-Z]+)([ ]*([+-]+|[*/^]?)([ ]*[+-^]*)?([0-9]+|[a-zA-Z]+))*$"

pattern = '^s'

name = "username"

print(re.match(pattern, name) is not None)