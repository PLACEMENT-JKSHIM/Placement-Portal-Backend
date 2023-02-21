from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render
# Create your views here.

def index(request):
    return render(request,"home/index.html")


def login(request):
<<<<<<< HEAD
    return render(request,"login.html")

def gallery(request):
    return render(request,"gallery.html")
=======
    return render(request,"home/login.html")
>>>>>>> c823a09bff894591012ff02adb5a0e92fbeb17dc
