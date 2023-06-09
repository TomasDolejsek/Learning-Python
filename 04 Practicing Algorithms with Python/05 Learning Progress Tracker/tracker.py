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
    def __init__(self):
        self.notifies = dict()
        super().__init__()

    def new_item(self, values):
        id = ('0000' + f"{self.howmany + 1}")[-5:]
        super().new_item(id, Student(values[0], values[1], values[2]))
        print("The student has been added.")        
    
    def update_item(self, id, points):
        self.data[id].update_points(points)
        self.check_if_completed(id)
        
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

    def check_if_completed(self, id):
        limits = dict([(cou, lim.limit) for cou, lim in courses.data.items()])
        for course, points in self.data[id].c_points.items():
            if points >= limits[course]:
                if id not in self.notifies.keys():
                    self.notifies[id] = [course,]
                else:
                    self.notifies[id].append(course)

    def notify(self):
        entries = len(self.notifies.keys())
        for id, finished in self.notifies.items():
            for course in finished:
                print(f"To: {self.data[id].email}")
                print("Re: Your Learning Progress")
                print(f"Hello, {self.data[id].firstname} {self.data[id].lastname}! ", end = '')
                print(f"You have accomplished our {course} course!")
        self.notifies.clear()
        print(f"Total {entries} students have been notified.")

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

    def display_statistics(self):
        popularity = dict()
        activity = dict()
        complexity = dict()
        for key, course in self.data.items():
            popularity[key] = len(course.visitors)
            activity[key] = course.activity
            try:
                complexity[key] = 1 / (course.ptotal / course.activity)
            except ZeroDivisionError:
                complexity[key] = 0
        display, popularity = self.what_to_display(max(popularity.values(), default = 0), popularity)
        print(f"Most popular: {display}")
        display, popularity = self.what_to_display(min(popularity.values(), default = 0), popularity)
        print(f"Least popular: {display}")
        display, activity = self.what_to_display(max(activity.values(), default = 0), activity)
        print(f"Highest activity: {display}")
        display, activity = self.what_to_display(min(activity.values(), default = 0), activity)
        print(f"Lowest activity: {display}")
        display, complexity = self.what_to_display(min(complexity.values(), default = 0), complexity)
        print(f"Easiest course: {display}")
        display, complexity = self.what_to_display(max(complexity.values(), default = 0), complexity)
        print(f"Hardest course: {display}")

    def what_to_display(self, compare, some_ity):
        new_ity = some_ity
        if all(map(lambda x: x == 0, some_ity.values())):  # some_ity dict is empty
            text = 'n/a'
            return text, new_ity
        some_ity = dict(filter(lambda x: x[1] == compare, some_ity.items()))
        for key in some_ity:
            del new_ity[key]
        text = ', '.join(some_ity.keys())
        return text, new_ity

    def display_visitors(self, course):
        enrolled = dict()
        for id in self.data[course].visitors:
            points = students.data[id].c_points[course]
            completed = points / self.data[course].limit * 100
            enrolled[id] = (points, completed)
        enrolled = sorted(enrolled.items(), key=lambda x: (-x[1][0], x[0]))
        print(course)
        print("id\t\tpoints\tcompleted")
        for stud in enrolled:
            print(f"{stud[0]}\t{stud[1][0]}\t\t{stud[1][1]:.1f}%")

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
    def __init__(self):
        self.valid_commands = ('add students', 'add points', 'list', 'find', 'statistics', 'notify', 'back', 'exit')
        super().__init__("Learning Progress Tracker.")
    
    def start(self):
        while True:
            user = input().lower()
            if not user.strip():
                print("No input")
                continue
            if user not in self.valid_commands:
                print("Unknown command!")
                continue
            if user == self.valid_commands[0]:
                AddStudentsMenu()
                continue
            if user == self.valid_commands[1]:
                AddPointsMenu()
                continue
            if user == self.valid_commands[2]:
                students.display_keys()
                continue
            if user == self.valid_commands[3]:
                FindMenu()
                continue
            if user == self.valid_commands[4]:
                StatisticsMenu()
                continue
            if user == self.valid_commands[5]:
                students.notify()
                continue
            if user == self.valid_commands[-2]:
                print("Enter 'exit' to exit the program")
                continue
            if user == self.valid_commands[-1]:
                print("Bye!")
                exit()

class AddStudentsMenu(UserInterface):
    def __init__(self):
        self.valid_commands = ('back',)
        self.added = 0
        super().__init__("Enter student credentials or 'back' to return:")
    
    def start(self):
        validator = DataValidator()
        while True:
            user = input()
            if user == self.valid_commands[-1]:
                break
            user = user.split()
            validated_data = validator.validate_student_data(user)
            if not validated_data:
                continue
            students.new_item(validated_data)
            self.added += 1
        print(f"Total {self.added} students have been added.")

class AddPointsMenu(UserInterface):
    def __init__(self):
        self.valid_commands = ('back',)
        super().__init__("Enter an id and points or 'back' to return:")
    
    def start(self):
        validator = DataValidator()
        while True:
            user = input()
            if user == self.valid_commands[-1]:
                break
            user = user.split()
            if user[0] not in students.data.keys():
                print(f"No student is found for id={user[0]}.")
                continue
            validated_data = validator.validate_courses_points(user)
            if not validated_data:
                continue
            courses.update_all(user[0], validated_data)
            students.update_item(user[0], validated_data)
        
class FindMenu(UserInterface):
    def __init__(self):
        self.valid_commands = ('back',)
        super().__init__("Enter an id and points or 'back' to return:")
    
    def start(self):
        while True:
            user = input().strip()
            if user == self.valid_commands[-1]:
                break
            students.display_points(user)

class StatisticsMenu(UserInterface):
    def __init__(self):
        self.valid_commands = ('python', 'dsa', 'databases', 'flask', 'back')
        super().__init__("Type the name of a course to see details or 'back' to quit")

    def start(self):
        courses.display_statistics()
        while True:
            user = input().lower()
            if user not in self.valid_commands:
                print("Unknown course.")
                continue
            if user == self.valid_commands[0]:
                courses.display_visitors('Python')
                continue
            if user == self.valid_commands[1]:
                courses.display_visitors('DSA')
                continue
            if user == self.valid_commands[2]:
                courses.display_visitors('Databases')
                continue
            if user == self.valid_commands[3]:
                courses.display_visitors('Flask')
                continue
            if user == self.valid_commands[-1]:
                break

if __name__ == '__main__':
    students = StudentDatabase()
    courses = CourseDatabase()
    MainMenu()