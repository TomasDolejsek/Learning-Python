import re

class Student:
    def __init__(self, firstname, lastname, email):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.c_points = list()

    def __str__(self):
        return f"Student: {self.firstname} {self.lastname}. Email: {self.email}"

    def update_points(self, new_points):
        self.c_points = new_points
        print("Points updated.")

    def info(self):
        return "NEco"

def correct_input(input, valid_input):
    if input not in valid_input: return False
    else: return True
def add_student_menu():
    print("Enter student credentials or 'back' to return:")
    while True:
        data = input().split()
        if not data:
            print("Incorrect credentials")
            continue
        if data[0] == 'back':
            break
        if len(data) < 3:
            print("Incorrect credentials")
            continue
        if add_student(data):
            print("The student has been added")
            continue
    print(f"Total {len(students_dict)} students have been added.")
def add_student(data):
    emailpattern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    firstnamepattern = "^[a-zA-Z]+(-|')?[a-zA-Z]+$"
    lastnamepattern = "^[a-zA-Z]+((-|')?[ a-zA-Z]+)*(-|')?[a-zA-Z]+$"
    firstname = data[0]
    lastname = " ".join(data[1:-1])
    email = data[-1]
    student_id = ('00' + f"{len(students_dict) + 1}")[-3:]

    if not re.match(firstnamepattern, firstname):
        print("Incorrect first name.")
        return False
    if not re.match(lastnamepattern, lastname):
        print("Incorrect last name.")
        return False
    if not re.match(emailpattern, email):
        print("Incorrect email.")
        return False
    for id, student in students_dict.items():
        if student.email == email:
            print("This email is already taken.")
            return False
    students_dict[student_id] = Student(firstname, lastname, email)
    return True

def add_points_menu():
    points = list()
    print("Enter an id and points or 'back' to return")
    while True:
        data = input().strip().split()
        try:
            if data[0] == 'back':
                break
            if len(data) != 5: raise IndexError
            for number in data[1:]:
                if int(number) <= 0: raise ValueError
                else: points.append(int(number))
        except:
            print("Incorrect points format.")
            continue
        if data[0] not in students_dict.keys():
            print(f"No student is found for id={data[0]}.")
            continue
        students_dict[data[0]].update_points(points)

def list_students():
    print("Students:")
    if not students_dict:
        print("No students found.")
        return
    for id in students_dict.keys():
        print(id)

def find_points():
    courses = ('Python', 'DSA', 'Databases', 'Flask')
    print("Enter an id and points or 'back' to return")
    while True:
        id = input().strip()
        if id == 'back':
            break
        if id not in students_dict.keys():
            print(f"No student is found for id={id}.")
            continue
        print(f"{id} points: ", end = '')
        for i in range(len(courses)):
            print(f"{courses[i]}={students_dict[id].c_points[i]} ", end='')
        print()

def main_menu():
    while True:
        user_input = input()
        if not user_input.strip():
            print("No input")
            continue
        if not correct_input(user_input, valid_input):
            print("Unknown command!")
            continue
        if user_input == valid_input[0]:
            add_student_menu()
            continue
        if user_input == valid_input[1]:
            add_points_menu()
            continue
        if user_input == valid_input[2]:
            list_students()
            continue
        if user_input == valid_input[3]:
            find_points()
            continue
        if user_input == valid_input[-2]:
            print("Enter 'exit' to exit the program")
            continue
        if user_input == valid_input[-1]:
            print("Bye!")
            exit()

# main program
valid_input = ('add students', 'add points', 'list', 'find', 'back', 'exit')
print("Learning Progress Tracker.")
students_dict = dict()

if __name__ == '__main__':
    main_menu()