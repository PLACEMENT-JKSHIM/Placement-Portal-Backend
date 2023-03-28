from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date
# Create your models here.

class Company(models.Model):
     c_name=models.CharField( max_length=60,default='Company Name')
     about=models.CharField( max_length=1000,null=True,blank=True)
     image = models.ImageField(upload_to='images', default='blank.png')
     def __str__(self):
         return f"{self.c_name}" 

class Team(models.Model):
    mem_name=models.CharField( max_length=60,null=False)
    mem_designation=models.CharField( max_length=60,null=False)
    mem_image = models.ImageField(upload_to='teams',default='blank.png')
    mem_description=models.TextField(null=True,blank=True, default='')
    def __str__(self):
        return f"{self.mem_name}-{self.mem_designation}-{self.mem_image}-{self.mem_description}"
    
class Rule(models.Model):
    rule = models.TextField(null=False)
    def __str__(self):
        return f"{self.rule}"

class Slider(models.Model):
    slider_image=models.ImageField(upload_to='sliders')
    def __str__(self):
        return f"{self.slider_image}"


class Job(models.Model):
    class Status(models.TextChoices):
        OPEN = 'O'
        CLOSE = 'C'
    title=models.CharField(max_length=50,null=True)
    description=models.TextField(blank=True,null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    academic_year=models.IntegerField(validators=[MaxValueValidator(2100), MinValueValidator(2010)])
    sslc=models.DecimalField(max_digits=4, decimal_places=2,default=0.00)
    puc=models.DecimalField(max_digits=4, decimal_places=2,default=0.00)
    diploma=models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    degree=models.DecimalField(max_digits=4, decimal_places=2,default=0.00)
    curr_cgpa=models.DecimalField(max_digits=3, decimal_places=2,default=0.00)
    gap_edu=models.IntegerField(default=0)
    min_dob = models.DateField(validators=[MinValueValidator(date(1990, 1, 1))])
    max_dob = models.DateField(validators=[MaxValueValidator(date(2040, 1, 1))])
    ctc_pa=models.DecimalField(max_digits=15, decimal_places=2,default=0.00)
    max_activebacklog=models.IntegerField(default=0)
    max_histbacklog=models.IntegerField(default=0)
    # other_company=models.IntegerField() 
    registration_date=models.DateField()
    talk_date=models.DateField()
    interview_date=models.DateField()
    test_date=models.DateField()
    notes=models.TextField (blank=True,null=True)
    status=models.CharField(max_length=2,choices=Status.choices,default=Status.OPEN)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.company}-{self.title}"
