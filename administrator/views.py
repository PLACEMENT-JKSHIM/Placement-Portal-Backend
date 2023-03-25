import http
from django.forms.models import model_to_dict
from django.core import serializers
from django.shortcuts import render,redirect
from home.models import Slider,Team,Company,Job
from .forms import TeamForm, UserForm,SliderForm,JobForm,CompanyForm
from django.http import HttpResponse,JsonResponse
import json
from student.models import Student
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db import IntegrityError
from django.contrib import messages
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


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


def addJob(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save()
            messages.success(request, message=" {0} added Successfully!".format(job.title))
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    messages.error(request, message=f"{field} : {error}")
        return redirect('jobs')
    else:
        form = JobForm()
    context = {'form': form}
    return render(request, "admininstrator/company/addjob.html", context)

@login_required(login_url='/login')
def companies(request):
    companies=Company.objects.all()
    if request.method == 'POST':
        form = CompanyForm(request.POST,request.FILES)
        print(form)
        if form.is_valid():
            companynew = form.save()
            messages.success(request,message=" {0} deleted Successfully!".format(companynew))
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    messages.error(request, message=f"{field} : {error}")
            return redirect('admin')
    else:
        form = CompanyForm()
    return render(request, "admininstrator/company/companies.html",{'companies':companies})

def jobs(request):
    jobs=Job.objects.all()
    context={
        'jobs':jobs
    }
    return render(request, "admininstrator/company/jobs.html",context)


@login_required(login_url='/login')
def deletecompany(request,id):
    print(request.user.is_superuser)
    c=get_object_or_404(Company,id=id)
    cname=c.c_name
    c.delete()
    messages.success(request, message=" {0} deleted Successfully!".format(cname))
    return redirect('companies')

@login_required(login_url='/login')
def editCompany(request,id):
    company=get_object_or_404(Company,id=id)
    cname=company.c_name
    if request.method == 'GET':
        form=CompanyForm(instance=company)
        context={
            'form':form,
            'company':company
        }
        return render(request,"admininstrator/company/editCompany.html",context)
    if request.method=="POST":
        form = CompanyForm(request.POST,request.FILES, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, message=" {0} updated Successfully!".format(cname))
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    messages.error(request, message=f"{field} : {error}")
        return redirect('companies')
    return redirect('companies')



    