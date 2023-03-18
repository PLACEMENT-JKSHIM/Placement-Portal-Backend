from django.contrib import admin

# Register your models here.
from student.models import Student,PreviousJob


admin.site.register(Student)
admin.site.register(PreviousJob)