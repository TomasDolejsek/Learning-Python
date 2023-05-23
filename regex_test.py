import re

#"^[+-]?([0-9]+|[a-zA-Z]+)([ ]*([+-]+|[*/^]?)([ ]*[+-]*)?([0-9]+|[a-zA-Z]+))*$"
#"^[+-]?([0-9]+|[a-zA-Z]+)([ ]*([+-]+|[*/^]?)([ ]*[+-^]*)?([0-9]+|[a-zA-Z]+))*$"

pattern = '^Good [a-z]*$'

name = "Good evening!"

print(re.match(pattern, name) is not None)