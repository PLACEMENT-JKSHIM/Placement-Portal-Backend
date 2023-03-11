from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from .models import Company, Job
from django.shortcuts import render
# Create your views here.


def index(request):
    return render(request, "home/index.html")


def login(request):
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


def company(req):
    #testing 
    j = Job.objects.get(id=1)
    c = Company.objects.get(id=j.company.id)
    comp1 = Company.objects.get(id=j.company.id)
    # checking feilds
    job1= Job.objects.get(company=comp1.id)#comp1 holds object of company
    print(job1)
    return render(req, "dummy.html", {'c': c})