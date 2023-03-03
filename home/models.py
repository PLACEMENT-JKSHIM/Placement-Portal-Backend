from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Student(models.Model):

    class Status(models.TextChoices):
        EDITABLE = 'E'
        NON_EDITABLE = 'NE'
        LOGINB_LOCKED = 'LB'
        APPLICATION_BLOCKED = 'AB'


    u=models.OneToOneField(User,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=50,null=True)
    middle_name=models.CharField(max_length=50,null=True)
    last_name=models.CharField(max_length=50,null=True)
    status=models.CharField(max_length=2,choices=Status.choices,default=Status.EDITABLE)


class Company(models.Model):
     c_name=models.CharField( max_length=60,null=True)
     about=models.CharField( max_length=1000,null=True)
     image = models.ImageField(upload_to='images')
     def __str__(self):
         return f"{self.c_name}" 


class Jobs(models.Model):
    class Status(models.TextChoices):
        REG_OPEN = 'O'
        REG_CLOSE = 'C'
    title=models.CharField(max_length=50,null=True)
    description=models.CharField( max_length=100,null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    academic_year=models.IntegerField()
    sslc=models.DecimalField(max_digits=4, decimal_places=2)
    puc=models.DecimalField(max_digits=4, decimal_places=2)
    degree=models.DecimalField(max_digits=4, decimal_places=2)
    curr_cgpa=models.DecimalField(max_digits=2, decimal_places=2)
    gap_edu=models.IntegerField()
    min_dob=models.DateTimeField()
    max_dob=models.DateTimeField()
    ctc_pa=models.DecimalField(max_digits=15, decimal_places=2)
    max_activebacklog=models.IntegerField()
    max_histbacklog=models.IntegerField()
    other_company=models.IntegerField()
    registration_date=models.DateTimeField()
    talk_date=models.DateField()
    interview_date=models.DateField()
    test_date=models.DateField()
    notes=models.CharField( max_length=1000,null=True)
    status= status=models.CharField(max_length=2,choices=Status.choices,default=Status.REG_OPEN)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.company}-{self.title}"