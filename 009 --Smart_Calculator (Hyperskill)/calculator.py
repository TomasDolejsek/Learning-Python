def compute(num1, num2, operation):
    return num1 + num2 if operation == '+' else num1 - num2
    
def normalize_operator(operator):
    isplus = True
    for op in operator:
        if op not in valid_operators:
            return ValueError
        isplus = not isplus if op == '-' else isplus
    return '+' if isplus else '-'
        
# main program
valid_operators = {'+','-'}
while True:
    inp = input().split()
        
    if not inp: continue  # empty input
        
    elif inp[0] == '/help':
        print("Smart calculator. Usage: put + or - among numbers.")
        continue
    elif inp[0] == '/exit':
        print("Bye!")
        break
        
    try:
        result = int(inp[0])
        for i in range(1, len(inp) - 1, 2):
            result = compute(result, int(inp[i + 1]), normalize_operator(inp[i]))
    except ValueError:
        print("Wrong input!")
        continue
    print(result)