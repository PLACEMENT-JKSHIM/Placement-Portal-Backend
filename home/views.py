from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from .models import Company, Job, Rule, Slider, Team,Gallery
from administrator.models import Job_student,Statistic
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib import auth
from student.models import Student
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.db.models import Avg
# Create your views here.

@cache_page(60 * 60)
def index(request):
    sliders = Slider.objects.all()
    teams = Team.objects.all()
    gallery = Gallery.objects.all()
    statistics = Statistic.objects.all().first()
    return render(request, "home/index.html",context={'gallery':gallery,'sliders':sliders,'teams':teams,'statistics':statistics})


def login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.is_staff:   
            return redirect('/au')
        else:   
            return redirect('/home')
            
    if request.method=='POST':
        usn=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=usn,password=password)
        if user is not None:
            auth.login(request, user)
            if request.user.is_superuser or request.user.is_staff:
                messages.success(request, message='Successfully logged in')
                if request.GET.getlist("next"):
                    return redirect(to=request.GET.getlist("next")[0])
                else:    
                    return redirect('/au')
            s=Student.objects.filter(user=user).first()
            if s.status == 'LB':
                messages.error(request, message="Login blocked")
            else:
                if request.GET.getlist("next"):
                    return redirect(to=request.GET.getlist("next")[0])
                else:    
                    return redirect('/home')
        else:
            messages.error(request, message="Invaild username or password")
            
    return render(request, "home/login.html")



@login_required(login_url='/login',redirect_field_name=None)
def logout(request):
    auth.logout(request)
    return redirect('/login')