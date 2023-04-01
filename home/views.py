from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from .models import Company, Job, Rule, Slider, Team
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib import auth
from student.models import Student
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
# Create your views here.

# @cache_page(60 * 60)
def index(request):
    sliders = Slider.objects.all()
    teams = Team.objects.all()
    return render(request, "home/index.html",context={'sliders':sliders,'teams':teams})



def login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:   
            return redirect('/au')
        else:   
            return redirect('/student_home')
            
    if request.method=='POST':
        usn=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=usn,password=password)
        print(usn,password)
        if user is not None:
            auth.login(request, user)
            if request.user.is_superuser:
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
                    return redirect('/student_home')
        else:
            messages.error(request, message="Invaild username or password")
            
    return render(request, "home/login.html")

def gallery(request):
    return render(request, "home/gallery.html")


@login_required(login_url='/login')
def rules(request):
    srules = Rule.objects.all()
    return render(request, "student/rules.html",context={'srules':srules})

@login_required(login_url='/login')
def profile(request):
    return render(request, "student/profile.html")


@login_required(login_url='/login',redirect_field_name=None)
def logout(request):
    auth.logout(request)
    return redirect('/login')