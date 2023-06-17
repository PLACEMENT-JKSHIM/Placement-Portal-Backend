from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date
# Create your models here.

class Company(models.Model):
    c_name = models.CharField(max_length=60, blank=False, null=False, verbose_name='Company Name')
    about = models.CharField(max_length=1000, null=True, blank=True, verbose_name='About')
    image = models.ImageField(upload_to='images', blank=True,null=True, default=None,  verbose_name='Image')


    def __str__(self):
        return f"{self.c_name}" 

class Team(models.Model):
    mem_name = models.CharField(max_length=60, verbose_name='Member Name', null=False)
    mem_designation = models.CharField(max_length=60, verbose_name='Member Designation', null=False)
    mem_image = models.ImageField(upload_to='teams', blank=True,null=True, verbose_name='Member Image')
    mem_description = models.TextField(null=True, blank=True, default='', verbose_name='Member Description')

    def __str__(self):
        return f"{self.mem_name}-{self.mem_designation}"

class Rule(models.Model):
    rule = models.TextField(null=False, verbose_name='Rule')
    def __str__(self):
        return f"{self.rule}"

class Slider(models.Model):
    slider_image = models.ImageField(upload_to='sliders', verbose_name='Slider Image')
    def __str__(self):
        return f"{self.slider_image}"

class Gallery(models.Model):
    title = models.CharField(max_length=30, verbose_name='Gallery Title', null=False)
    description = models.CharField(max_length=100, verbose_name='Gallery Description')
    image= models.ImageField(upload_to='gallery', verbose_name='Gallery Image',null=False)
    def __str__(self):
        return f"{self.title}"

class YearBatch(models.Model):
    startYear = models.IntegerField(validators=[MaxValueValidator(2100), MinValueValidator(2010)], verbose_name='Academic Year')
    endYear = models.IntegerField(validators=[MaxValueValidator(2100), MinValueValidator(2010)], verbose_name='Academic Year')
    def __str__(self):
        return f"{self.startYear}-{self.endYear}"

class Job(models.Model):
    title = models.CharField(max_length=50, verbose_name='Job Title', null=True)
    description = models.TextField(blank=True, null=True, verbose_name='Job Description')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Company')
    sslc = models.DecimalField(max_digits=4, decimal_places=2, default=0.00, verbose_name='SSLC Percentage', validators=[MaxValueValidator(100), MinValueValidator(0)])
    puc = models.DecimalField(max_digits=4, decimal_places=2, default=0.00, verbose_name='PUC Percentage', validators=[MaxValueValidator(100), MinValueValidator(0)])
    diploma = models.DecimalField(max_digits=4, decimal_places=2, default=0.00, verbose_name='Diploma Percentage', validators=[MaxValueValidator(100), MinValueValidator(0)])
    degree = models.DecimalField(max_digits=4, decimal_places=2, default=0.00, verbose_name='Degree Percentage', validators=[MaxValueValidator(100), MinValueValidator(0)])
    curr_cgpa = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, verbose_name='Current CGPA',validators=[MinValueValidator(0.00), MaxValueValidator(10.00)])
    gap_edu = models.IntegerField(default=0, verbose_name='Gap in Education (in years)')
    min_dob = models.DateField(blank=True,null=True,validators=[MinValueValidator(date(1990, 1, 1))], verbose_name='Minimum Date of Birth')
    max_dob = models.DateField(blank=True,null=True,validators=[MaxValueValidator(date(2040, 1, 1))], verbose_name='Maximum Date of Birth')
    ctc_pa = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, verbose_name='CTC per Annum')
    max_activebacklog = models.IntegerField(default=0, verbose_name='Maximum Active Backlogs')
    max_histbacklog = models.IntegerField(default=0, verbose_name='Maximum Previous Backlogs')
    registration_last_date = models.DateTimeField(verbose_name='Registration Last Date')
    talk_date = models.DateField(verbose_name='Talk Date')
    interview_date = models.DateField(verbose_name='Interview Date')
    test_date = models.DateField(verbose_name='Test Date')
    notes = models.TextField(blank=True, null=True, verbose_name='Notes')
    reg_open = models.BooleanField(default=True, verbose_name='Is Registration Open?')
    yearBatch=models.ForeignKey(YearBatch, on_delete=models.CASCADE, verbose_name='Academic Year Batch')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Created Date')
    updated = models.DateTimeField(auto_now=True, verbose_name='Last Updated Date')

    def __str__(self):
        return f"{self.company} - {self.title}"
    
