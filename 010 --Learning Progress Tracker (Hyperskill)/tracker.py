import re

class Database:
    def __init__(self):
        self.data = dict()
        self.howmany = 0
        
    def __str__(self):
        text_out = ''
        for key, value in self.data.items():
            text_out += f"{key}: {value}\n"
        return text_out
    
    def new_item(self, id, item):
        self.data[id] = item
        self.howmany += 1
        
    def update_item(self, id, item):
        self.data[id] = item
        
    def display_keys(self):
        for id in self.data.keys():
            print(id) 

class StudentDatabase(Database):
    def new_item(self, values):
        id = ('0000' + f"{self.howmany + 1}")[-5:]
        super().new_item(id, Student(values[0], values[1], values[2]))
        print("The student has been added.")        
    
    def update_item(self, id, points):
        self.data[id].update_points(points)
        
    def display_keys(self):
        print("Students:")
        if not students.data:
            print("No students found.")
            return
        super().display_keys()
    
    def display_points(self, id):
        if id not in self.data.keys():
            print(f"No student is found for id={id}.")
            return
        print(f"{id} points: ", end = '')
        for course, points in self.data[id].c_points.items():
            print(f"{course}={points} ", end='')
        print()

class CourseDatabase(Database):
    def __init__(self):
        self.data = {"Python": Course(600),
                      "DSA": Course(400),
                      "Databases": Course(480),
                      "Flask": Course(550)
                      }
        self.howmany = 4
    
    def update_all(self, student_id, new_points):
        i = 0
        for name in self.data.keys():
            if new_points[i] != 0:  # new course activity
                self.data[name].update_course(student_id, new_points[i])
            i += 1

class Student:
    def __init__(self, firstname, lastname, email):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.c_points = {'Python': 0, 'DSA': 0, 'Databases': 0, 'Flask': 0}

    def __str__(self):
        return f"Student: {self.firstname} {self.lastname}. Email: {self.email} Points: {self.c_points}"

    def update_points(self, new_points):
        i = 0
        for course in self.c_points.keys():
            self.c_points[course] += new_points[i]
            i += 1
        print("Points updated.")

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

class DataValidator:
    def __init__(self):
        self.emailpattern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        self.firstnamepattern = "^[a-zA-Z]+(-|')?[a-zA-Z]+$"
        self.lastnamepattern = "^[a-zA-Z]+((-|')?[ a-zA-Z]+)*(-|')?[a-zA-Z]+$"

    def validate_student_data(self, valdata):
        if len(valdata) < 3:
            print("Incorrect credentials")
            return False
        
        firstname = valdata[0]
        lastname = " ".join(valdata[1:-1])
        email = valdata[-1]
        
        if not re.match(self.firstnamepattern, firstname):
            print("Incorrect first name.")
            return False
        if not re.match(self.lastnamepattern, lastname):
            print("Incorrect last name.")
            return False
        if not re.match(self.emailpattern, email):
            print("Incorrect email.")
            return False
        for student in students.data.values():
            if student.email == email:
                print("This email is already taken.")
                return False
        return (firstname, lastname, email)
    
    def validate_courses_points(self, valdata):
        points = list()
        try:
            if len(valdata) != 5:
                raise ValueError
            for number in valdata[1:]:
                if int(number) < 0:
                    raise ValueError
                points.append(int(number))
            return points
        except ValueError:
            print("Incorrect points format.")
            return False

class UserInterface:
    def __init__(self, greeting):
        if greeting:
            print(greeting)
        self.start()
        
    def start(self):
        pass

class MainMenu(UserInterface):
    def __init__(self, greeting):
        self.valid_commands = ('add students', 'add points', 'list', 'find', 'back', 'exit')
        super().__init__(greeting)
    
    def start(self):
        while True:
            user = input()
            if not user.strip():
                print("No input")
                continue
            if user not in self.valid_commands:
                print("Unknown command!")
                continue
            if user == self.valid_commands[0]:
                menu = AddStudentsMenu("Enter student credentials or 'back' to return:")
                continue
            if user == self.valid_commands[1]:
                menu = AddPointsMenu("Enter student credentials or 'back' to return:")
                continue
            if user == self.valid_commands[2]:
                students.display_keys()
                continue
            if user == self.valid_commands[3]:
                menu = FindMenu("Enter student credentials or 'back' to return:")
                continue
            if user == self.valid_commands[-2]:
                print("Enter 'exit' to exit the program")
                continue
            if user == self.valid_commands[-1]:
                print("Bye!")
                exit()
    
class AddStudentsMenu(UserInterface):
    def __init__(self, greeting):
        self.valid_commands = ('back',)
        self.added = 0
        super().__init__(greeting)
    
    def start(self):
        while True:
            user = input().split()
            if not user:
                continue
            if user[0] == self.valid_commands[-1]:
                break
            validator = DataValidator()
            validated_data = validator.validate_student_data(user)
            if not validated_data:
                continue
            students.new_item(validated_data)
            self.added += 1
        print(f"Total {self.added} students have been added.")

class AddPointsMenu(UserInterface):
    def __init__(self, greeting):
        self.valid_commands = ('back',)
        super().__init__(greeting)
    
    def start(self):
        while True:
            user = input().split()
            if not user[0]:
                continue
            if user[0] == self.valid_commands[-1]:
                break
            if user[0] not in students.data.keys():
                print(f"No student is found for id={user[0]}.")
                continue
            validator = DataValidator()
            validated_data = validator.validate_courses_points(user)
            if not validated_data:
                continue
            courses.update_all(user[0], validated_data)  # databases updates    
            students.update_item(user[0], validated_data)
        
class FindMenu(UserInterface):
    def __init__(self, greeting):
        self.valid_commands = ('back',)
        super().__init__(greeting)
    
    def start(self):
        while True:
            user = input().split()
            if not user:
                continue
            if user[0] == self.valid_commands[-1]:
                break
            students.display_points(user[0])
        
students = StudentDatabase()
courses = CourseDatabase()
if __name__ == '__main__':
    main_menu = MainMenu("Learning Progress Tracker.")