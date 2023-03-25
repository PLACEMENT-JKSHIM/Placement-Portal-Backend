from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from .models import Company, Job
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib import messages
from student.models import Student
from home.models import Job
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):
    return render(request, "home/index.html")


def login(request):
    if request.method=='POST':
        usn=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=usn,password=password)
        if user is not None:
            auth.login(request, user)
            if request.user.is_superuser:
                messages.success(request, message='Successfully logged in')
                return redirect("/au")
            s=Student.objects.filter(user=user).first()
            if s.status == 'LB':
                messages.error(request, message="Login blocked")
            else:
                return redirect("/home")
        else:
            messages.error(request, message="Invaild username or password")
            
    return render(request, "home/login.html")


def home(request):
    return render(request, "student/student_home.html")


def gallery(request):
    return render(request, "home/gallery.html")


def rules(request):
    return render(request, "student/rules.html")


def profile(request):
    return render(request, "student/profile.html")


def changePassword(request):
    return render(request, "student/changePassword.html")


def registerCompany(request):
    jobs = Job.objects.all()
    return render(request, "student/registerCompany.html",{'jobs': jobs})