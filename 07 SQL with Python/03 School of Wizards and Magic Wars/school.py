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
