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