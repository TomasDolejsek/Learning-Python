best students = """
select name from students
join Student_Subject on students.student_id = Student_Subject.student_id
where grade = 3
group by name
having avg(result) = 5
"""