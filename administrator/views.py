import http
from django.forms.models import model_to_dict
from django.core import serializers
from django.shortcuts import render,redirect
from home.models import Slider, Team
from .forms import TeamForm, UserForm,SliderForm
from django.http import HttpResponse,JsonResponse
import json
from student.models import Student,PreviousJob
from home.models import Job
from administrator.models import Notice,Job_student
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db import IntegrityError
from django.contrib import messages
from django.core.cache import cache
from django.contrib.auth import authenticate, login,get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
import json
import zipfile
import os
import io
from django.conf import settings

User = get_user_model()
heads=['USN']
unwanted=['id','user','editable','created_at','updated_at','status','job_student','image','resume','previousjob']
for s in Student._meta.get_fields():
    if s.name not in unwanted:
        heads.append(s.verbose_name)

heads.append('Previous Experience')

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

@login_required
def changePasswordAdmin(request):
    if request.method == 'POST':
        # get the input values from the POST request
        username = request.POST.get('username')
        new_password = request.POST.get('newpassword')
        confirm_password = request.POST.get('confirmpassword')

        # perform basic form validation
        if not all([username, new_password, confirm_password]):
            messages.error(request, 'All fields are required')
        elif new_password != confirm_password:
            messages.error(request, 'Passwords do not match')
        else:
            # find the user and update the password
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            messages.success(request, f'Password updated successfully for user {username}')
            return redirect('changePasswordAdmin')

    return render(request, 'admininstrator/student/changePasswordAdmin.html')

def addNewsUpdates(request):
    if request.method=='POST':
        title=request.POST.get("news_title")
        content=request.POST.get("news_content")
        addNewsUpdates=Notice(title=title,content=content)
        addNewsUpdates.save()
    return render(request,"admininstrator/admin_newsUpdates.html")

def deleteTeamMember(request,id):
    teamobj=get_object_or_404(Team,id=id)
    teamobj.delete()
    messages.success(request, message="Member deleted successfully")
    return redirect('/au/adminEditor')

def deleteSlider(request,id):
    print(id)
    slidobj = get_object_or_404(Slider,id=id)
    slidobj.delete()
    messages.success(request, message="Slider image deleted successfully")
    return redirect('/au/adminEditor')

def registerHome(request):
    jobs=Job.objects.all()
    selected={'id':-1}
        
    students = zip([],[])

    return render(request,"admininstrator/registerList.html",context={'heads':heads,'jobs':jobs,'students':students,'selected':selected,})


def registerList(request,id):
    students=[]
    pjs=[]
    selected={'id':id}
    jobs=Job.objects.all()
    if id==0:
        jobSt=Job_student.objects.all().select_related('student','student__user')
        selected['job']='ALL'
    else:
        job=get_object_or_404(Job,id=id)
        jobSt=Job_student.objects.filter(job=job).select_related('student','student__user')
        selected['job']=str(job)
    for j in jobSt:
        students.append(j.student)
        pjs.append(PreviousJob.objects.filter(user=j.student.user))
        
    students = zip(students, pjs)

    return render(request,"admininstrator/registerList.html",context={'heads':heads,'jobs':jobs,'students':students,'selected':selected,})
    

def downLoadResumes(request,id):
    if id==0:
        jobSt=Job_student.objects.all().select_related('student','student__user')
    else:
        job=get_object_or_404(Job,id=id)
        jobSt=Job_student.objects.filter(job=job).select_related('student','student__user')
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for jb in jobSt:
            if not jb.student.resume:
                continue
            file_path = os.path.join(settings.MEDIA_ROOT, str(jb.student.resume))
            zip_file.write(file_path, jb.student.user.username+".pdf")

    zip_buffer.seek(0)

    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment;filename="resume.zip"'
    return response

def downLoadImages(request,id):
    if id==0:
        jobSt=Job_student.objects.all().select_related('student','student__user')
    else:
        job=get_object_or_404(Job,id=id)
        jobSt=Job_student.objects.filter(job=job).select_related('student','student__user')

    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for jb in jobSt:
            if not jb.student.resume:
                continue
            file_path = os.path.join(settings.MEDIA_ROOT, str(jb.student.image))
            zip_file.write(file_path, jb.student.user.username+'.jpg')

    zip_buffer.seek(0)

    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment;filename="images.zip"'
    return response