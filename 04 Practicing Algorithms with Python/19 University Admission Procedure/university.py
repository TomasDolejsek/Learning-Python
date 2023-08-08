class Applicant:
    def __init__(self, data):
        self.name = ' '. join(data[:2])
        self.skills = [int(x) for x in data[2:6]]
        self.priorities = data[6:]

    def __str__(self):
        return f"{self.name} {self.skills} {self.priorities}"

    def skills_mean(self, skill_ids):
        summary = 0
        for skill_id in skill_ids:
            summary += self.skills[skill_id]
        return summary / len(skill_ids)


class Department:
    def __init__(self, name, skills):
        self.name = name
        self.required_skills = skills
        self.accepted_students = []

    @property
    def nstudents(self):
        return len(self.accepted_students)


class University:
    def __init__(self):
        self.SKILL_INDEXES = {'physics': 0, 'chemistry': 1, 'math': 2, 'computer science': 3}
        self.departments = []
        self.create_departments()
        self.start()

    def create_departments(self):
        self.departments.append(Department('Biotech', ['chemistry', 'physics']))
        self.departments.append(Department('Chemistry', ['chemistry']))
        self.departments.append(Department('Engineering', ['computer science', 'math']))
        self.departments.append(Department('Mathematics', ['math']))
        self.departments.append(Department('Physics', ['physics', 'math']))

    def start(self):
        naccepted = int(input())
        applicants = []
        with open('Data/applicants.txt') as file:
            for line in file:
                applicants.append(Applicant(line.split()))

        for i in range(0, 2):
            for depart in self.departments:
                remaining = sorted(applicants, key=lambda x: (-float(x[depart.skill_index]), x[0]))
                for applicant in remaining:
                    if depart.nstudents == naccepted:
                        break
                    if applicant[i] == depart.name:
                        depart.accepted_students.append(applicant)
                        applicants.remove(applicant)

        self.display_departments()

    @staticmethod
    def count_mean(skill_1, skill_2):
        return (skill_1 + skill_2) / 2

    def display_departments(self):
        for depart in self.departments:
            print(depart.name)
            for student in sorted(depart.accepted_students, key=lambda x: (-float(x[2]), x[0])):
                print(f"{student[0]} {student[1]} {student[2]}")
            print()


if __name__ == "__main__":
    University()
