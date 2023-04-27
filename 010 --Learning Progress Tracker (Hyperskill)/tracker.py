import re

class Student:
    counter = 0
    def __init__(self,firstname,lastname,email):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.counter += 1

    def __str__(self):
        return f"Student: {self.firstname} {self.lastname}. Email: {self.email}"

    def how_many_students(self):
        return self.counter

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
    print(f"Total {len(students)} students have been added.")

def add_student(data):
    emailpattern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    firstnamepattern = "^[a-zA-Z]+(-|')?[a-zA-Z]+$"
    lastnamepattern = "^[a-zA-Z]+((-|')?[ a-zA-Z]+)*(-|')?[a-zA-Z]+$"
    firstname = data[0]
    lastname = " ".join(data[1:-1])
    email = data[-1]

    if not re.match(firstnamepattern, firstname):
        print("Incorrect first name.")
        return False

    if not re.match(lastnamepattern, lastname):
        print("Incorrect last name.")
        return False
    if not re.match(emailpattern, email):
        print("Incorrect email.")
        return False
    students.append(Student(firstname, lastname, email))
    return True

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
            print("Bye!")
            exit()
        if user_input == valid_input[1]:
            add_student_menu()
            continue
        if user_input == valid_input[2]:
            print("Enter 'exit' to exit the program")
            continue

# main program
valid_input = ['exit','add students','back']
print("Learning Progress Tracker.")
students = list()

if __name__ == '__main__':
    main_menu()