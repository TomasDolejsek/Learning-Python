class Applicant:
    def __init__(self, data):
        self.name = ' '. join(data[:2])
        self.skills = [float(x) for x in data[2:7]]
        self.priorities = data[7:]

    def __str__(self):
        return f"{self.name} {self.skills} {self.priorities}"

    def get_score(self, skill_names):
        indexes = {'physics': 0, 'chemistry': 1, 'math': 2, 'computer science': 3}
        result = 0
        for name in skill_names:
            result += self.skills[indexes[name]]
        result /= len(skill_names)
        if self.skills[4] > result:
            result = self.skills[4]
        return result


class Department:
    def __init__(self, name, skills):
        self.name = name
        self.required_skills = skills
        self.accepted_students = []

    def __str__(self):
        text = list()
        for student in sorted(self.accepted_students, key=lambda x: (-x.get_score(self.required_skills), x.name)):
            text.append(f"{student.name} {student.get_score(self.required_skills)}")
        text.append('')
        return '\n'.join(text)

    @property
    def nstudents(self):
        return len(self.accepted_students)


class University:
    def __init__(self):
        self.departments = self.create_departments()
        self.start()

    @staticmethod
    def create_departments():
        departs = list()
        departs.append(Department('Biotech', ['chemistry', 'physics']))
        departs.append(Department('Chemistry', ['chemistry']))
        departs.append(Department('Engineering', ['computer science', 'math']))
        departs.append(Department('Mathematics', ['math']))
        departs.append(Department('Physics', ['physics', 'math']))
        return departs

    def start(self, verbose=True):
        naccepted = int(input())
        applicants = []
        with open('Data/applicants.txt', 'r') as file:
            for line in file:
                applicants.append(Applicant(line.split()))
        for i in range(0, 3):
            for depart in self.departments:
                remaining = sorted(applicants, key=lambda x: (-x.get_score(depart.required_skills), x.name))
                for applicant in remaining:
                    if depart.nstudents == naccepted:
                        break
                    if applicant.priorities[i] == depart.name:
                        depart.accepted_students.append(applicant)
                        applicants.remove(applicant)
        if verbose:
            self.display_department_students()
        self.save_results()

    def display_department_students(self):
        for department in self.departments:
            print(department.name)
            print(department)

    def save_results(self):
        for department in self.departments:
            filename = department.name.lower()+'.txt'
            with open(filename, 'w') as file:
                file.write(department.__str__())
        print("Results have been saved.")


if __name__ == "__main__":
    University()
