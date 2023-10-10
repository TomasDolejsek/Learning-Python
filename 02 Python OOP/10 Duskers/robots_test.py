import re

def check_graphical_robots(robots_display, number_of_robots) \
        -> bool:
    result = True
    if number_of_robots == 0:
        return True

    if len(robots_display) == 0:
        return False

    positions = []
    prev_position = -1
    while robots_display[0].find("|", prev_position + 1) != -1:
        prev_position = robots_display[0].find("|", prev_position + 1)
        positions.append(prev_position)
    if len(positions) != number_of_robots - 1:
        return False

    for line in robots_display:
        stripped_lines = [robot_line.strip() for robot_line in re.split("\|", line)]
        print(len(stripped_lines))

        if len(stripped_lines) != number_of_robots:
            return False

        prev_position = -1
        for pos in positions:
            if line.find("|", prev_position + 1) != pos:
                return False
            prev_position = pos

        result = result and all(
            (robot == stripped_lines[0] and (robot != "" or number_of_robots == 0)) for robot in stripped_lines[1:])

    return result

ROBOT = ("           __             ",
         "   _(\    [@@]            ",
         "  (__/\__ \--/ __         ",
         "     \___/----\  \   __   ",
         "         \ }{ /\  \_/ _\  ",
         "         /\__/\ \__O (__  ",
         "        (--/\--)    \__/  ",
         "        _)(  )(_          ",
         "       `---''---`         ")

lines = []
for line in ROBOT:
    print(f"{line}|{line}|{line}")
    lines.append(f"{line}|{line}|{line}")
print(check_graphical_robots(lines, 3))
    