import re

class Student:
    def __init__(self, firstname, lastname, email):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.c_points = {'Python': 0, 'DSA': 0, 'Databases': 0, 'Flask': 0}

    def __str__(self):
        return f"Student: {self.firstname} {self.lastname}. Email: {self.email} Points: {self.c_points}"

    def add_points(self, new_points):
        i = 0
        for course in self.c_points.keys():
            self.c_points[course] += new_points[i]
            i += 1
        print("Points updated.")

class StudentDatabase:
    def __init__(self):
        self.sdata = dict()
        self.howmany = 0    
    
    def __str__(self):
        text_out = ''
        for key, value in self.sdata.items():
            text_out += f"{key}: {value}\n"
        return text_out
    
    def add_student(self, values):
        self.sdata[values[0]] = Student(values[1], values[2], values[3])
        self.howmany += 1
        print("The student has been added.")        

    def update_points(self, student_id, new_points):
        self.sdata[student_id].add_points(new_points)

class Course:
    def __init__(self, limit):
        self.limit = limit
        self.activity = 0
        self.ptotal = 0
        self.visitors = set()

    def update_course(self, student_id, points_to_add):
        self.activity += 1
        self.ptotal += points_to_add
        self.visitors.add(student_id)

class CoursesDatabase:
    def __init__(self):
        self.cdata = {"Python": Course(600),
                      "DSA": Course(400),
                      "Databases": Course(480),
                      "Flask": Course(550)
                      }

    def update_courses(self, student_id, new_points):
        i = 0
        for name in self.cdata.keys():
            if new_points[i] != 0:  # new course activity
                self.cdata[name].update_course(student_id, new_points[i])
            i += 1

def correct_input(input, valid_input):
    if input not in valid_input: return False
    else: return True

def correct_student_data(valdata):
    emailpattern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    firstnamepattern = "^[a-zA-Z]+(-|')?[a-zA-Z]+$"
    lastnamepattern = "^[a-zA-Z]+((-|')?[ a-zA-Z]+)*(-|')?[a-zA-Z]+$"
    firstname = valdata[0]
    lastname = " ".join(valdata[1:-1])
    email = valdata[-1]
    student_id = ('0000' + f"{students.howmany + 1}")[-5:]

    if not re.match(firstnamepattern, firstname):
        print("Incorrect first name.")
        return False
    if not re.match(lastnamepattern, lastname):
        print("Incorrect last name.")
        return False
    if not re.match(emailpattern, email):
        print("Incorrect email.")
        return False
    for student in students.sdata.values():
        if student.email == email:
            print("This email is already taken.")
            return False
    return (student_id, firstname, lastname, email)

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
        validated_data = correct_student_data(data)
        if not validated_data:
            continue
        students.add_student(validated_data)
        print(f"Total {students.howmany} students have been added.")

def add_points_menu():
    print("Enter an id and points or 'back' to return")
    while True:
        points = list()
        user = input().strip().split()
        try:
            if user[0] == 'back':
                break
            if user[0] not in students.sdata.keys():
                print(f"No student is found for id={data[0]}.")
                continue
            if len(user) != 5: raise IndexError
            for number in user[1:]:
                if int(number) <= 0: raise ValueError
                else: points.append(int(number))
        except:
            print("Incorrect points format.")
            continue
        courses.update_courses(user[0], points)  # databases updates    
        students.update_points(user[0], points)
        
def list_students():
    print("Students:")
    if not students.sdata:
        print("No students found.")
        return
    for id in students.sdata.keys():
        print(id)

def find_points():
    print("Enter an id and points or 'back' to return")
    while True:
        id = input().strip()
        if id == 'back':
            break
        if id not in students.sdata.keys():
            print(f"No student is found for id={id}.")
            continue
        print(f"{id} points: ", end = '')
        for course, points in students.sdata[id].c_points.items():
            print(f"{course}={points} ", end='')
        print()

def main_menu():
    valid_input = ('add students', 'add points', 'list', 'find', 'back', 'exit')
    print("Learning Progress Tracker.")
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

students = StudentDatabase()
courses = CoursesDatabase()
if __name__ == '__main__':
    main_menu()
