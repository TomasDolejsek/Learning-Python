import re

pattern = '^(0[1-9]|1[0-9]|2[0-3]):([0-5][0-9])$'

text = '14:00'

print(re.search(pattern, text) is not None)
    
self.stops = {1: 'Prospekt Avenue',
                      2: 'Pilotow Street',
                      3: 'Elm Street',
                      4: 'Bourbon Street',
                      5: 'Fifth Avenue',
                      6: 'Sunset Boulevard',
                      7: 'Sesame Street'}