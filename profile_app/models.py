from django.db import models
from django.contrib.auth.models import User

time_start_choice = (
    (8,8),(9,9),(10,10),(11,11),(12,12),
    (1,1),(2,2),(3,3)
)

time_end_choice = (
    (9,9),(10,10),(11,11),(12,12),
    (1,1),(2,2),(3,3),(4,4)
)

class time_slots(models.Model):
    start_time = models.IntegerField(choices=time_start_choice)
    end_time = models.IntegerField(choices=time_end_choice)

    def __str__(self):
        return 'from {} to {}'.format(self.start_time,self.end_time)

gender_choice = (
    ('Male','Male'),
    ('Female','Female')
)

profile_type_choice = (
    ('Student','Student'),
    ('Teacher','Teacher')
)

session_choice = (
    ('2017','2017'),('2018','2018'),('2019','2019'),('2020','2020'),
    ('2021','2021'),('2022','2022'),('2023','2023'),('2024','2024')
)

semester_choice = (
    ('Fall','Fall'),
    ('Spring','Spring'),
)

class profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    department_name = models.ForeignKey('info_app.department',on_delete=models.CASCADE,null=True,blank=True)
    dob = models.DateField(null=True)
    gender = models.CharField(max_length=10,choices=gender_choice)
    cnic = models.CharField(max_length=20)
    profile_type = models.CharField(max_length=20,choices=profile_type_choice)
    from_semester = models.CharField(max_length=10,choices=semester_choice,blank=True,null=True)
    from_session = models.CharField(max_length=10,choices=session_choice,blank=True,null=True)
    # if teacher
    preferred_slots = models.ManyToManyField('profile_app.time_slots',blank=True)
    
    def __str__(self):
        return self.user.username + ' is a ' + self.profile_type
