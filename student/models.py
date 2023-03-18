from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator 


class Rule(models.Model):
     rule=models.TextField(null=False)
     def __str__(self):
         return f"{self.rule}" 

# Create your models here.

#usn
#name as in aadhar
#name as in 10 marks card
#gender
#contact number
#alternative number
#personal email id
#aadhar card number
#pancard number
#dob
#home town
#home town state
#permanent address
#10th percentage,10th board ,school,year
#12th percentage,10th board ,college,year
#degree percentage
#degree stream 
#degree course
#degree college name
#degree university
#MBA specialisation
#MBA CGPA
#MBA SGPA1
#MBA SGPA2
#MBA SGPA3
#MBA SGPA4
#college location (auto filled)
# Past experience yes/no
#if yes role , duration,company
# projects or interships if any
#resume
#passport size photo
#created at
#updated at
#active_backlog
#total backlog
#status:login blocked,application blocked


class Student(models.Model):

    class Blocked(models.TextChoices):
        NOT_BLOCKED='N'
        LOGIN_BLOCKED = 'LB'
        APPLICATION_BLOCKED = 'AB'

    class Gender(models.TextChoices):
        MALE='M'
        FEMALE='F'

    class PreGraduate(models.TextChoices):
        PU='P'
        DIPLOMA='D'

    class Specialisation(models.TextChoices):
        Finance='F'
        HR='HR'


    user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    status=models.CharField(blank=True,max_length=2,choices=Blocked.choices,default=Blocked.NOT_BLOCKED)
    editable=models.BooleanField(default=True)

    name=models.CharField(blank=True,max_length=50)
    nameAadhar=models.CharField(blank=True,max_length=50)
    gender=models.CharField(blank=True,max_length=1,choices=Gender.choices,default=Gender.MALE)
    image=models.ImageField(blank=True,null=True)
    resume=models.FileField(blank=True,null=True)

    phoneNo=models.CharField(blank=True,max_length=11)
    alternatePhoneNo=models.CharField(blank=True,max_length=11)
    email=models.EmailField(blank=True,max_length=50)
    aadhar=models.CharField(blank=True,max_length=12)
    pancard= models.CharField(blank=True,max_length=12)

    dateOfBirth=models.DateField(blank=True,null=True)
    homeTown=models.CharField(blank=True,max_length=50)
    homeState=models.CharField(blank=True,max_length=50)
    permanentAddress=models.CharField(blank=True,max_length=150)
    
    tenPercentage=models.FloatField(blank=True,null=True)
    tenBoard=models.CharField(blank=True,max_length=10)
    tenSchool=models.CharField(blank=True,max_length=50)
    tenPassYear=models.PositiveSmallIntegerField(blank=True,null=True,validators=[MinValueValidator(1950),MaxValueValidator(2040)])
    tenState=models.CharField(blank=True,max_length=50)
    tenCountry=models.CharField(blank=True,max_length=50)

    puOrDiploma=models.CharField(max_length=1,choices=PreGraduate.choices,default=PreGraduate.PU)
    twelvePercentage=models.FloatField(blank=True,null=True)
    twelveBoard=models.CharField(blank=True,max_length=10)
    twelveSchool=models.CharField(blank=True,max_length=50)
    twelvePassYear=models.PositiveSmallIntegerField(blank=True,null=True,validators=[MinValueValidator(1950),MaxValueValidator(2040)])
    twelveState=models.CharField(blank=True,max_length=50)
    twelveCountry=models.CharField(blank=True,max_length=50)

    degreePercentage=models.FloatField(blank=True,null=True)
    degreeStream=models.CharField(blank=True,max_length=30)
    degreCourse=models.CharField(blank=True,max_length=30)
    degreeCollege=models.CharField(blank=True,max_length=50)
    degreeUniversity=models.CharField(blank=True,max_length=50)
    degreePassYear=models.PositiveSmallIntegerField(blank=True,null=True,validators=[MinValueValidator(1950),MaxValueValidator(2040)])
    degreeState=models.CharField(blank=True,max_length=50)
    degreeCountry=models.CharField(blank=True,max_length=50)

    mbaSpecialisation=models.CharField(blank=True,max_length=2,choices=Specialisation.choices)
    sgpa1=models.FloatField(blank=True,null=True)
    sgpa2=models.FloatField(blank=True,null=True)
    sgpa3=models.FloatField(blank=True,null=True)
    sgpa4=models.FloatField(blank=True,null=True)
    cgpa=models.FloatField(blank=True,null=True)

    activeBacklog=models.IntegerField(blank=True,default=0)
    totalBacklog=models.IntegerField(blank=True,default=0)

    pastExperience=models.BooleanField(default=False)

    projects=models.TextField(blank=True)

    preferredJobLocation=models.CharField(blank=True,max_length=30)

    created_at=models.DateTimeField(editable=False,default=datetime.now())
    updated_at=models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.user.username