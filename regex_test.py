import re

#"^[+-]?([0-9]+|[a-zA-Z]+)([ ]*([+-]+|[*/^]?)([ ]*[+-]*)?([0-9]+|[a-zA-Z]+))*$"
#"^[+-]?([0-9]+|[a-zA-Z]+)([ ]*([+-]+|[*/^]?)([ ]*[+-^]*)?([0-9]+|[a-zA-Z]+))*$"

pattern = '^_{0,2}[a-z]([a-z0-9_]*)*$'

name = "very_long_name"

print(re.match(pattern, name) is not None)