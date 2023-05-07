from collections import deque

expression = '(-32) + (6+2) *2^2' + ' '
op_priorities = {'-': 1, '+': 1, '*': 2, '/': 2, '^': 3}

def normalize_operator(operator):
    if '-' in operator or '+' in operator:
        if operator.count('-') % 2 == 1:
            return '-'
        else: 
            return '+'
    else:
        return operator

def compute(num1, num2, operator):
    if operator == '-':
        return num1 - num2
    elif operator == '+':
        return num1 + num2
    elif operator == '*':
        return num1 * num2
    elif operator == '/':
        return num1 // num2
    else:
        return num1 ** num2

members = list()
i = 0
while i < len(expression):
    member = ''
    if expression[i] == ' ':
        i += 1
        continue
    elif expression[i] == '(' or expression[i] == ')':
        members.append(expression[i])
        i += 1
        continue
    elif expression[i] in op_priorities:
        while expression[i] in op_priorities:
            member += expression[i]
            i += 1
        members.append(normalize_operator(member))
        continue  
    while expression[i].isalpha():
        member += expression[i] 
        i += 1
    while expression[i].isnumeric():
        member += expression[i]
        i += 1
    members.append(member)
    
postfix = deque()
stack = deque()
for member in members:
    if member.isnumeric():
        postfix.append(member)
        continue
    if member in op_priorities:
        if len(stack) == 0 or stack[-1] == '(':
            stack.append(member)
            continue
        if op_priorities[member] > op_priorities[stack[-1]]:
            stack.append(member)
            continue
        if op_priorities[member] <= op_priorities[stack[-1]]:
            while True:
                if not stack:
                    break
                if stack[-1] == '(':
                    break
                if op_priorities[member] > op_priorities[stack[-1]]:
                    break
                poped = stack.pop()
                postfix.append(poped)
            stack.append(member)
            continue
    if member == '(':
        stack.append(member)
        continue    
    if member == ')':
        while True:
            poped = stack.pop()
            if poped == '(':
                break
            postfix.append(poped)
        continue 
for _ in range(len(stack)):
    postfix.append(*[stack.pop(),]) 

for member in postfix:
    if member.isnumeric():
        stack.append(member)
        continue
    if member in op_priorities:
        n1 = stack.pop()
        n2 = stack.pop()
        result = compute(int(n2), int(n1), member)
        stack.append(result)
        
print(postfix)
print(stack)