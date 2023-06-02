# Tic Tac Toe

def display_playfield():
    print('-' * (grid_size * 2 + 3))
    for i in range(grid_size):
        print("| ", end = '')
        for stone in playfield[i]:
            print(f"{stone} ", end = '')
        print("|")
    print('-' * (grid_size * 2 + 3))
    
def display_result(result):
    if result == 0:
        print("Draw")
    elif result == 1:
        print("X wins")
    elif result == 2:
        print("O wins")
    else:
        pass
    
def whats_the_state(rplayed):
    result = int()
    for line in playfield:
        result = check_line(line)
        if result < 3:
            return result
    
    for ncolumn in range(grid_size):
        result = check_column(ncolumn)
        if result < 3:
            return result

    result = check_main_diagonal()
    if result < 3:
        return result

    result = check_side_diagonal()
    if result < 3:
        return result

    if rplayed == grid_size ** 2:
        return 0  # draw            
    
    return result  # result = 3

def check_line(line):
    if line.count('X') == grid_size:
        return 1  # 'X' wins
    elif line.count('O') == grid_size:
        return 2  # 'O' wins
    else:
        return 3  # no winner yet

def check_column(cnumber):
    column = list()
    for i in range(grid_size):
        column.append(playfield[i][cnumber])
    return check_line(column)
    
def check_main_diagonal():
    diagonal = list()
    for i in range(grid_size):
        for j in range(grid_size):
            if i == j:
                diagonal.append(playfield[i][j])
    return check_line(diagonal)

def check_side_diagonal():
    diagonal = list()
    for i in range(grid_size):
        for j in range(grid_size):
            if i == j:
                diagonal.append(playfield[i][-j - 1])
    return check_line(diagonal)
        
def correct_input(instring):
    global xcoord, ycoord
    try:
        xcoord, ycoord = instring.split()
        xcoord = int(xcoord) - 1 
        ycoord = int(ycoord) - 1
    except ValueError:
        print("You should enter two numbers!")
        return False
    if not ((0 <= xcoord <= grid_size - 1) and (0 <= ycoord <= grid_size - 1)):
        print(f"Coordinates should be from 1 to {grid_size}!")       
        return False
    if playfield[xcoord][ycoord] in 'XO':
        print("This cell is occupied! Choose another one!")
        return False
    return True
    
# main program
grid_size = 3  # constant for now
playfield = [[' '] * grid_size for _ in range(grid_size)]  # empty playfield
xcoord = int()
ycoord = int()
x_plays = True  # False = 'O' plays
round_number = 0

display_playfield()
while True:
    while True:
        if correct_input(input()):
            break
    if x_plays:
        playfield[xcoord][ycoord] = 'X'
    else:
        playfield[xcoord][ycoord] = 'O'
    round_number += 1
    x_plays = not x_plays
    display_playfield()
    state = whats_the_state(round_number)
    if state != 3:
        display_result(state)
        break