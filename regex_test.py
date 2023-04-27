import re
pattern = "^[a-zA-Z]+(-|')?[a-zA-Z]+$"

name = "John-"

print(re.match(pattern, name) is not None)