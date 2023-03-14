from django.shortcuts import render,redirect
from .forms import UserForm
from django.http import HttpResponse
import json
from student.models import Student
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib import messages

def index(request):
    return render(request, "admininstrator/index.html")

def addStudent(request):
    if request.method=='POST' and request.POST.get('students'):
        data=json.loads(request.POST.get('students'))
        try:
            for d in data:
                u,success=User.objects.get_or_create(username=d['username'],password=d['password'])
                if not success:
                    continue
                u.save()
                s=Student.objects.create(user=u)
                s.save()
        except:
            messages.error(request, message={'title':"username",'message':"no column username"})
            messages.error(request, message={'title':"password",'message':"no column password"})
        else:
            messages.success(request, message={'message':"added successfully"})

        # data=[User(username=d['username'],password=d['password']) for d in data]
        # users=User.objects.bulk_create(data,ignore_conflicts=True)
        # students=[Student(user=user) for user in users]
        # print(students)
        # Student.objects.bulk_create(students,ignore_conflicts=True)


    elif request.method=='POST':
        form=UserForm(request.POST)

        if form.is_valid():
            user=form.save()
            Student(user=user).save()
            messages.success(request, message={'message': "Saved successfully"})
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    messages.error(request, message={'message':error,'title':field})
    form=UserForm()

    return render(request, "admininstrator/student/add.html",context={'student':form})

def adminEditor(request):
    return render(request, "admininstrator/adminEditor.html")