best students = """
select name from students
join Student_Subject on students.student_id = Student_Subject.student_id
where grade = 3
group by name
having avg(result) = 5
"""

achievement_point = """
select name, sum(bonus) as 'bonus point' from students 
join Student_Achievement on students.student_id = Student_Achievement.student_id
join Achievement on Student_Achievement.achievement_id = Achievement.achievement_id
group by name
order by sum(bonus) desc
limit 4
"""

average_student = """
select name, CASE
             when avg(result) > 3.5 then 'above average'
             else 'below average'
             end as best
from Students
join Student_Subject on Students.student_id = Student_Subject.student_id
group by name
"""

best_of_department = """
select name, department_name from Department
join Students using (department_id)
join Student_Subject using (student_id)
group by name
having avg(result) > 4.5
order by name
"""
