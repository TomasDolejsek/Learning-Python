import re

text = '01/13/2999'
pattern = r'(0[1-9]|1[0-9]|2[0-9]|3[0-1])/(0[1-9]|1[0-2])/[1-2]+\d{3}'

print(re.search(pattern, text) is not None)
    
