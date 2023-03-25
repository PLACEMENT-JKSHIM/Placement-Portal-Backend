from django.db import models

# Create your models here.
from home.models import Job
from student.models import Student


class Job_student(models.Model):
    class Status(models.TextChoices):
        APPLIED = 'A'
        OFFERED = 'O'
        REJECTED = 'R'
        QUALIFIED = 'Q'
    job = models.OneToOneField(Job, on_delete=models.CASCADE)
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    status=models.CharField(max_length=2,choices=Status.choices,default=Status.APPLIED)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.job}-{self.student}-{self.status}"


class Notice(models.Model):
    
    title=models.CharField( max_length=60,null=False)
    content=models.CharField( max_length=1000,null=False)
    created_on =models.DateTimeField( auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)
    def __str__(self):
         return f"{self.title}" 