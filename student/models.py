from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from home.models import YearBatch
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.core.exceptions import ValidationError
import home.models as m


def validate_file_size(value):
    filesize= value.size
    
    if filesize > 512*1024:
        raise ValidationError("You cannot upload file more than 500KB")
    else:
        return value

class Branch(models.Model):
    branchname1 = models.CharField(max_length=100)
    branchname2 =models.CharField(blank=True,null=True,max_length=100)

    def __str__(self):
        if self.branchname2:
            return f"{self.branchname1}-{self.branchname2}"
        else:
            return self.branchname1

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

    def upload_student(instance,filename):
        return m.generate_unique_filename(instance, filename, 'student')
    
    def upload_resume(instance,filename):
        return m.generate_unique_filename(instance, filename, 'resume')

    user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    status=models.CharField(blank=True,max_length=2,choices=Blocked.choices,default=Blocked.NOT_BLOCKED)
    editable=models.BooleanField(default=True)

    name=models.CharField(blank=True,max_length=50,verbose_name='Name as in 10th marks card')
    nameAadhar=models.CharField(blank=True,max_length=50,verbose_name='Name as in Aadhar card')
    gender=models.CharField(max_length=1,choices=Gender.choices,default=Gender.MALE,verbose_name="Gender")
    image=models.ImageField(blank=True,null=True,upload_to=upload_student,validators=[validate_file_size])
    resume=models.FileField(blank=True,null=True,upload_to=upload_resume,validators=[validate_file_size])
    branch=models.ForeignKey(Branch,blank=True,null=True, on_delete=models.SET_NULL,verbose_name="Branch")
    phoneNo=models.IntegerField(blank=True,null=True,verbose_name="Phone number",validators=[MinValueValidator(1000000000),MaxValueValidator(99999999999)])
    alternatePhoneNo=models.IntegerField(blank=True,null=True,verbose_name="Alternate Phone number",validators=[MinValueValidator(1000000000),MaxValueValidator(99999999999)])
    email=models.EmailField(blank=True,max_length=50,verbose_name="Personal Email ID")
    aadhar=models.CharField(blank=True,max_length=12,verbose_name="Aadhar card number")
    pancard= models.CharField(blank=True,max_length=12,verbose_name="Pancard number")

    dateOfBirth=models.DateField(blank=True,null=True,verbose_name="Date of birth")
    homeTown=models.CharField(blank=True,max_length=50,verbose_name="Home town")
    homeState=models.CharField(blank=True,max_length=50,verbose_name="Home town state")
    address=models.TextField(blank=True,verbose_name="Permanent address")
    
    tenPercentage=models.FloatField(default=0.0,validators=[MinValueValidator(0),MaxValueValidator(100)],verbose_name="10th percentage")
    tenBoard=models.CharField(blank=True,max_length=10,verbose_name="10th board")
    tenSchool=models.CharField(blank=True,max_length=50,verbose_name="10th school")
    tenPassYear=models.PositiveSmallIntegerField(blank=True,null=True,validators=[MinValueValidator(1950),MaxValueValidator(2040)],verbose_name="10th pass year")
    tenState=models.CharField(blank=True,max_length=50,verbose_name="10th state")
    tenCountry=models.CharField(blank=True,max_length=50,verbose_name="10th country")

    twelvePercentage=models.FloatField(default=0.0,validators=[MinValueValidator(0),MaxValueValidator(100)],verbose_name="12th percentage")
    twelveBoard=models.CharField(blank=True,max_length=10,verbose_name="12th board")
    twelveSchool=models.CharField(blank=True,max_length=50,verbose_name="12th college")
    twelvePassYear=models.PositiveSmallIntegerField(blank=True,null=True,validators=[MinValueValidator(1950),MaxValueValidator(2040)],verbose_name="12th pass year")
    twelveState=models.CharField(blank=True,max_length=50,verbose_name="12th state")
    twelveCountry=models.CharField(blank=True,max_length=50,verbose_name="12th country")

    diplomaPercentage=models.FloatField(default=0.0,validators=[MinValueValidator(0),MaxValueValidator(100)],verbose_name="Diploma percentage")
    diplomaBoard=models.CharField(blank=True,max_length=10,verbose_name="Diploma board")
    diplomaSchool=models.CharField(blank=True,max_length=50,verbose_name="Diploma college")
    diplomaPassYear=models.PositiveSmallIntegerField(blank=True,null=True,validators=[MinValueValidator(1950),MaxValueValidator(2040)],verbose_name="Diploma pass year")
    diplomaState=models.CharField(blank=True,max_length=50,verbose_name="Diploma state")
    diplomaCountry=models.CharField(blank=True,max_length=50,verbose_name="Diploma country")

    degreePercentage=models.FloatField(default=0.0,validators=[MinValueValidator(0),MaxValueValidator(100)],verbose_name="Degree percentage")
    degreeStream=models.CharField(blank=True,max_length=30,verbose_name="Degree stream")
    degreeCourse=models.CharField(blank=True,max_length=30,verbose_name="Degree course")
    degreeCollege=models.CharField(blank=True,max_length=50,verbose_name="Degree college")
    degreeUniversity=models.CharField(blank=True,max_length=50,verbose_name="Degree university")
    degreePassYear=models.PositiveSmallIntegerField(blank=True,null=True,validators=[MinValueValidator(1950),MaxValueValidator(2040)],verbose_name="Degree pass year")
    degreeState=models.CharField(blank=True,max_length=50,verbose_name="Degree state")
    degreeCountry=models.CharField(blank=True,max_length=50,verbose_name="Degree country")

    sgpa1=models.FloatField(default=0.0,validators=[MinValueValidator(0),MaxValueValidator(10)],verbose_name="SGPA 1")
    sgpa2=models.FloatField(default=0.0,validators=[MinValueValidator(0),MaxValueValidator(10)],verbose_name="SGPA 2")
    sgpa3=models.FloatField(default=0.0,validators=[MinValueValidator(0),MaxValueValidator(10)],verbose_name="SGPA 3")
    sgpa4=models.FloatField(default=0.0,validators=[MinValueValidator(0),MaxValueValidator(10)],verbose_name="SGPA 4")
    cgpa=models.FloatField(default=0.0,validators=[MinValueValidator(0),MaxValueValidator(10)],verbose_name="CGPA")

    activeBacklog=models.IntegerField(blank=True,default=0,validators=[MinValueValidator(0)],verbose_name="Number of Active backlogs")
    totalBacklog=models.IntegerField(blank=True,default=0,validators=[MinValueValidator(0)],verbose_name="Number of Total backlogs")
    gap_edu=models.IntegerField(blank=True,default=0,validators=[MinValueValidator(0)],verbose_name="Total gap in education")
    yearBatch=models.ForeignKey(YearBatch, on_delete=models.CASCADE, verbose_name='Academic Year Batch')
    projects=models.TextField(blank=True,verbose_name="Projects decription")

    preferredJobLocation=models.CharField(blank=True,max_length=30,verbose_name="Preferred job location")

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def delete(self, *args, **kwargs):
        self.user.delete()
        return super(self.__class__, self).delete(*args, **kwargs)
    
    def __str__(self):
        return self.user.username
     

class PreviousJob(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    role=models.CharField(max_length=50,verbose_name="Role")
    yearsofExperience=models.IntegerField(default=0,verbose_name="Years of Experience")
    monthsofExperience=models.IntegerField(default=0,verbose_name="Months of Experience")
    company=models.CharField(max_length=50,verbose_name="Company Name")

    def __str__(self):
        return self.role

