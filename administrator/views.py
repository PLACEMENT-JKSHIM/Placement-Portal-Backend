import http
from django.forms.models import model_to_dict
from django.core import serializers
from django.shortcuts import render,redirect
from home.models import Slider, Team
from .forms import TeamForm, UserForm,SliderForm,JobForm
from django.http import HttpResponse,JsonResponse
import json
from student.models import Student
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db import IntegrityError
from django.contrib import messages
from django.core.cache import cache


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
    
    elif request.method=='POST':
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

def blockStudent(request):
    students = Student.objects.all().order_by('-updated_at')[:5]
    return render(request,"admininstrator/blockStudent.html",{'students':students})

def editBlock(request):
    query = request.GET.get('q', '')#get the query
    students = []
    users = User.objects.filter(username__icontains=query) if query else []
    for user in users:
        if student := Student.objects.filter(user=user).first():
            # convert Student object to a dictionary
            user_dict = {
                'id': student.user.id,
                'user': student.user.username
            }
            student_dict = {
                'editable': student.editable,
                'user': user_dict,
                'name': student.name,
                # add any other fields you want to include here
            }
            students.append(student_dict)
    print(students)
    context = {'students': students}
    return JsonResponse(context, safe=False)

def profileEditBlock(request,id):
    user=User.objects.get(id=id)
    student=Student.objects.get(user=user)
    student.editable = student.editable == False
    student.save()
    return redirect("blockStudent")

def profileEditBlockAll(req):
    Student.objects.all().update(editable=False)
    return redirect("blockStudent")

def profileEditUnblockAll(req):
    Student.objects.all().update(editable=True)
    return redirect("blockStudent")

#company
def addcompany(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save()
            # Redirect to a success page or do something else
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobForm()
    context = {'form': form}
    return render(request, "admininstrator/company/addCompany.html", context)

    