from django.shortcuts import render,redirect
from home.models import Slider, Team
from .forms import TeamForm, UserForm,SliderForm
from django.http import HttpResponse
import json
from student.models import Student
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db import IntegrityError
from django.contrib import messages


def index(request):
    return render(request, "admininstrator/index.html")

def addStudent(request):
    if request.method=='POST' and request.POST.get('students'):
        data=json.loads(request.POST.get('students'))
        error=False
        for d in data:
            print(d)
            form=UserForm(d)
            if form.is_valid():
                user=form.save(commit=False)
                user.set_password(str(d['password']))
                user.save()
                Student(user=user).save()
            else:
                error=True
                for field,errors in form.errors.items():
                    for error in errors:
                        messages.error(request, message=f"{field} {d['username']} : {error}")
        
        if not error:
            messages.success(request, message="added successfully")
        else:
            messages.success(request, message="added others successfully")


    elif request.method=='POST':
        form=UserForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(request.POST['password'])
            user.save()
            Student(user=user).save()
            messages.success(request, message="Saved successfully")
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    messages.error(request, message=f"{field} : {error}")
    form=UserForm()

    return render(request, "admininstrator/student/add.html",context={'student':form})

def adminEditor(request):
    if request.method=='POST' and  request.FILES.get('slider_image') :
        form = SliderForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            # Slider(slider=slider).save()
            messages.success(request, message="Image added successfully")
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    messages.error(request, message=f"{field} : {error}")
    
    if request.method=='POST':
        form = TeamForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, message="Member added successfully")
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    messages.error(request, message=f"{field} : {error}")

    sliderForm=SliderForm()
    teamForm=TeamForm()
    members = Team.objects.all()
    sliders = Slider.objects.all()
    return render(request, "admininstrator/adminEditor.html",context={'members':members,'sliders':sliders,'sliderForm':sliderForm,'teamForm':teamForm})