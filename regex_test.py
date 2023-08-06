import re

pattern = '^[de]$'

text = 'E'

print(re.search(pattern, text) is not None)