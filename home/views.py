from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from .models import Company, Job
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib import auth
from student.models import Student
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    return render(request, "home/index.html")

def login(request):
    if request.method=='POST':
        usn=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=usn,password=password)
        print(usn,password)
        if user is not None:
            auth.login(request, user)
            if request.user.is_superuser:
                messages.success(request, message='Successfully logged in')
                return redirect("/au")
            s=Student.objects.filter(user=user).first()
            if s.status == 'LB':
                messages.error(request, message="Login blocked")
            else:
                return redirect("/student_home")
        else:
            messages.error(request, message="Invaild username or password")
            
    return render(request, "home/login.html")

# @login_required(login_url='/login')
# def home(request):
#     return render(request, "student/student_home.html")


def gallery(request):
    return render(request, "home/gallery.html")


def rules(request):
    return render(request, "student/rules.html")


@login_required(login_url='/login')
def profile(request):
    return render(request, "student/profile.html")

