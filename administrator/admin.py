from django.contrib import admin
from .models import Job_student, Notice,Statistic,Job_branch

# Register your models here.
admin.site.register(Job_student)
admin.site.register(Notice)
admin.site.register(Statistic)
admin.site.register(Job_branch)