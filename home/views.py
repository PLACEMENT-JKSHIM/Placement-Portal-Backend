from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render
# Create your views here.

def index(request):
    return render(request,"home/index.html")


def login(request):
    return render(request,"home/login.html")

def home(request):
    return render(request,"student/student_home.html")

def gallery(request):
    return render(request,"home/gallery.html")

def profile(request):
    return render(request,"student/profile.html")
