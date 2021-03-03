from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from profile_app.models import profile

class department(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

semester_choice = (
    ('Fall','Fall'),
    ('Spring','Spring'),
)

session_choice = (
    ('2017','2017'),('2018','2018'),('2019','2019'),('2020','2020'),
    ('2021','2021'),('2022','2022'),('2023','2023'),('2024','2024')
)

semester_year_choice = (
    ('2021','2021'),('2022','2022'),('2023','2023'),('2024','2024'),
    ('2025','2025'),('2026','2026'),('2027','2027'),('2028','2028'),
)
    
def thifunc():
    retval = []
    objs = User.objects.all()
    for i in objs:
        a = profile.objects.get(user=i)
        if a.profile_type == 'Teacher':
            retval.append(i.id)
    return {'id__in':retval}

class course(models.Model):
    name = models.CharField(max_length=200)
    credit_hour = models.IntegerField(default=1)
    contact_hour = models.IntegerField(default=1)
    from_department = models.ForeignKey('info_app.department',on_delete=models.CASCADE)
    for_semester = models.CharField(max_length=10,choices=semester_choice)
    for_semester_year = models.CharField(max_length=10,choices=semester_year_choice)
    for_session = models.CharField(max_length=10,choices=session_choice)
    taught_by = models.ForeignKey(User,on_delete=models.CASCADE,limit_choices_to=thifunc)
    section_capacity = models.IntegerField(default=20)

    def __str__(self):
        return self.name + ' by ' + self.from_department.name

section_choice = (
    ('A','A'),('B','B'),('C','C'),('D','D')
)

def thifunc2():
    retval = []
    objs = User.objects.all()
    for i in objs:
        a = profile.objects.get(user=i)
        if a.profile_type == 'Student':
            retval.append(i.id)
    return {'id__in':retval}

class sections_offered(models.Model):
    name = models.CharField(max_length=1,choices=section_choice,default='A')
    for_course = models.ForeignKey('info_app.course',on_delete=models.CASCADE,null=True,blank=True)
    students = models.ManyToManyField(User,blank=True,limit_choices_to=thifunc2)

    def __str__(self):
        return 'Section ' + self.name + ' for ' + self.for_course.name

grades_choice = (
    ('A+','A+'),('A','A'),('A-','A-'),('B+','B+'),('B','B'),('B-','B-'),
    ('C+','C+'),('C','C'),('C-','C-'),('D+','D+'),('D','D'),('D-','D-'),
    ('F','F'),('I','I'),('W','W')
)

class result(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    course = models.ForeignKey('info_app.course',on_delete=models.CASCADE)
    grade = models.CharField(max_length=2,choices=grades_choice)

    def __str__(self):
        return self.user.username + ' in ' + self.course.name