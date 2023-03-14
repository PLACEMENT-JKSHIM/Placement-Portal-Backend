from django.shortcuts import render,redirect

from home.models import Slider, Team
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
        data=[User(username=d['username'],password=d['password']) for d in data]
        User.objects.bulk_create(data,ignore_conflicts=True)
        messages.success(request, message={'message':"added successfully"})

    elif request.method=='POST':
        form=UserForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, message={'message': "Saved successfully"})
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    messages.error(request, message={'message':error,'title':field})
    form=UserForm()

    return render(request, "admininstrator/student/add.html",context={'student':form})

def adminEditor(request):
    members = Team.objects.all()
    sliders = Slider.objects.all()
    return render(request, "admininstrator/adminEditor.html",{'members':members,'sliders':sliders})