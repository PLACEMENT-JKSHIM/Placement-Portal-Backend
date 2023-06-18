import http
from django.db.models import Max,Avg
from django.forms.models import model_to_dict
from django.core import serializers
from django.shortcuts import render,redirect
from home.models import Slider,Team,Company,Job,Rule,Gallery
from .forms import TeamForm, UserForm,StaffForm,SliderForm,JobForm,CompanyForm,NewsForm,RuleForm,UpdateMarksForm,GalleryForm,YearBatchForm,BranchForm,StatisticForm
from django.http import HttpResponse,JsonResponse
import json
from student.models import Student,PreviousJob,Branch
from home.models import Job,YearBatch
from administrator.models import Notice,Job_student,Statistic,Job_branch
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db import IntegrityError
from django.contrib import messages
from django.core.cache import cache
from django.contrib.auth import authenticate, login,get_user_model,logout
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required,user_passes_test
from django.forms.models import model_to_dict
import json
import zipfile
import os
import io
from django.conf import settings
from django.http import Http404
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.utils.timezone import datetime,timezone
from django.db.models import Count,Q

#GLOBALS
statistic_obj = Statistic.objects.all()[0]
heads=['USN']
unwanted=['id','user','editable','created_at','updated_at','status','job_student','image','resume','previousjob']
for s in Student._meta.get_fields():
    if s.name not in unwanted:
        heads.append(s.verbose_name)

heads.append('Previous Experience')



def superuser_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f'/login?next={request.path}')
        if not request.user.is_superuser:
            raise Http404
        return view_func(request, *args, **kwargs)
    return wrapped_view

def staff_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f'/login?next={request.path}')
        if not request.user.is_staff:
            raise Http404
        return view_func(request, *args, **kwargs)
    return wrapped_view

@staff_required 
def index(request):
    user=request.user
    student_count = Student.objects.count()
    toppers = Student.objects.all().order_by('-cgpa')[:10]
    active_jobs=Job.objects.filter(reg_open=True).count()
    login_blocked_count = Student.objects.filter(status__exact='LB').count()
    app_blocked_count = Student.objects.filter(status__exact='AB').count()
    recently_updated=Student.objects.all().order_by('-updated_at')[:10]
    context={
        'student_count':student_count,
        'toppers':toppers,
        'login_blocked_count':login_blocked_count,
        'app_blocked_count':app_blocked_count,
        'active_jobs':active_jobs,
        'recently_updated':recently_updated,
        'user':user,
    }
    return render(request, "administrator/index.html",context)

import threading

def do_background_work(users):
    # do some work here
    print(users)
    return
    

@superuser_required
def addStudent(request):
    if request.method=='POST' and request.POST.get('students'):
        if not request.POST.get('yearBatch'):
            messages.error(request, message=f"Year Batch is required")
            return redirect(to='addStudent')

        yearBatch=YearBatch.objects.filter(pk=request.POST['yearBatch']).first()
        if not yearBatch:
            messages.error(request, message=f"Year Batch is required")
            return redirect(to='addStudent')
            
        data=json.loads(request.POST.get('students'))
        error=False
        for i,d in enumerate(data):
            if not d.get('username') or not d.get('password'):
                messages.error(request, message=f"Row {i} password and username is required")
                continue
            d['yearBatch']=yearBatch
            form=UserForm(d)
            if form.is_valid():
                user=form.save(commit=False)
                user.set_password(str(d['password']))
                user.save()
                Student(user=user,yearBatch=yearBatch).save()
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
            Student(user=user,yearBatch=YearBatch.objects.filter(pk=request.POST['yearBatch']).first()).save()
            messages.success(request, message="Added successfully")
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    messages.error(request, message=f"{field} : {error}")
    form=UserForm()

    return render(request, "administrator/student/add.html",context={'student':form})

@superuser_required
def updateStudent(request):
    form=UpdateMarksForm()
    if request.method=="POST" and request.POST.get("newusn"):
        if not request.POST.get("usn"):
            messages.error(request, message=f"Username is required")
        else:
            usn=request.POST.get("usn")
            newusn=request.POST.get("newusn")

            user=User.objects.filter(username=usn,is_superuser=False).first()
            olduser=User.objects.filter(username=newusn).first()
            if user:
                if not olduser:
                    user.username=newusn
                    user.save()
                    messages.success(request, message=f"Student {usn} updated to {newusn}")
                else:
                    messages.error(request, message=f"Student {newusn} already exists")
            else:
                messages.error(request, message=f"Student {usn} does not exists")

    elif request.method=="POST":
        usn=request.POST.get("usn")
        if not usn:
            messages.error(request, message=f"Username is required")
        else:
            user=User.objects.filter(username=usn,is_superuser=False).first()
            if user:
                form=UpdateMarksForm(request.POST,instance=user.student)
                if form.is_valid():
                    form.save()
                    messages.success(request, message=f"Studnet {usn} marks updated successfully")
                    form=UpdateMarksForm()
                else:
                    for field,errors in form.errors.items():
                        for error in errors:
                            messages.error(request, message=f"{field} : {error}")
            else:
                messages.error(request, message=f"Student {usn} does not exists")

    return render(request, "administrator/student/update.html",context={'form':form})

@superuser_required
def updateMultipleUsn(request):
    if request.method=='POST':
        if request.POST.get('usns'):
            data=json.loads(request.POST.get('usns'))
            error=False
            for i,d in enumerate(data,start=1):
                if d.get('username') and d.get('newusername'):
                    user=User.objects.filter(username=d['username'],is_superuser=False).first()
                    olduser=User.objects.filter(username=d['newusername']).first()
                    if user:
                        if not olduser:
                            user.username=d['newusername']
                            user.save()
                        else:
                            error=True
                            messages.error(request, message=f"Student {d['newusername']} already exists")
                    else:
                        error=True
                        messages.error(request, message=f"Student {d['username']} does not exists")
                else:
                    error=True
                    messages.error(request, message=f"Username is required at row {i}")
            if not error:
                messages.success(request, message="updated successfully")
            else:
                messages.success(request, message="updated others successfully")

    return redirect(to='/au/student/update')
@superuser_required
def updateMultipleMarks(request):
    if request.method=='POST':
        if request.POST.get('marks'):
            data=json.loads(request.POST.get('marks'))
            usns=[]
            marks=[]
            for d in data:
                if d.get('username'):
                    usns.append(d['username'])
                    m = {}
                    for key in ['sgpa1','username', 'sgpa2', 'sgpa3', 'sgpa4', 'cgpa']:
                        if key in d:
                            m[key] = d[key]
                    marks.append(m)

            students=Student.objects.filter(user__username__in=usns).select_related('user')
            for s in students:
                for m in marks:
                    if s.user.username==m['username']:
                        if m.get('sgpa1'):setattr(s, 'sgpa1',m['sgpa1'] )
                        if m.get('sgpa2'):s.sgpa2=m['sgpa2']
                        if m.get('sgpa3'):s.sgpa3=m['sgpa3']
                        if m.get('sgpa4'):s.sgpa4=m['sgpa4']
                        if m.get('cgpa'):s.cgpa=m['cgpa']
                        break
            
            for student in students:
                try:
                    student.full_clean()
                except ValidationError as e:
                    for key in e.message_dict:
                        for error in e.message_dict[key]:
                            messages.error(request, message=f"Student {student.user.username} {key} : {error}")
                    students=students.exclude(pk=student.pk)

            Student.objects.bulk_update(students, fields=['sgpa1', 'sgpa2', 'sgpa3', 'sgpa4', 'cgpa'])

            error=False
            errorUsns=""
            for d in data:
                if d.get('username'):
                    for s in students:
                        if s.user.username==d['username']:
                            break
                    else:
                        error=True
                        messages.error(request, message=f"Student {d['username']} may not exist")

            if not error:
                messages.success(request, message="updated successfully")
            else:

                messages.success(request, message="updated others successfully")

    return redirect(to='/au/student/update')

@superuser_required
def blockStudent(request):
    students = Student.objects.all().order_by('-updated_at')[:5]
    return render(request,"administrator/blockStudent.html",{'students':students})

@superuser_required
def editBlock(request):
    if request.method == 'POST':
        query = json.loads(request.body).get('q', '')
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
                    'image':{
                        'url':student.image.url if student.image else None
                    },
                'status':student.status
                    # add any other fields you want to include here
                }
                students.append(student_dict)
        context = {'students': students}
        return JsonResponse(context, safe=False)
    

@superuser_required
def profileEditBlock(request,id):
    user=get_object_or_404(User,id=id)
    student=get_object_or_404(Student,user=user)
    student.editable = student.editable == False
    student.save()
    return redirect("blockStudent")


@superuser_required
def loginBlockEdit(request,id):
    user=get_object_or_404(User,id=id)
    student=get_object_or_404(Student,user=user)
    student.status = 'N' if student.status=='LB' else 'LB'#this and the logic below,though they follow the different approach,yeild same expexted output
    student.save()
    return redirect("blockStudent")

@superuser_required
def applyBlockEdit(request,id):
    user=get_object_or_404(User,id=id)
    student=get_object_or_404(Student,user=user)
    if student.status in ['N', 'LB']:
        student.status = 'AB'
    elif student.status == 'AB':
        student.status = 'N'
    student.save()
    return redirect("blockStudent")

@superuser_required
def profileEditBlockAll(req):
    Student.objects.all().update(editable=False)
    return redirect("blockStudent")

@superuser_required
def profileEditUnblockAll(req):
    Student.objects.all().update(editable=True)
    return redirect("blockStudent")

#Login Block for all students
@superuser_required
def LoginBlockAll(req):
    Student.objects.all().update(status='LB')
    return redirect("blockStudent")

@superuser_required
def LoginUnblockAll(req):
    Student.objects.all().update(status='N')
    return redirect("blockStudent")

#applying block for all students
@superuser_required
def applyBlockAll(req):
    Student.objects.all().update(status='AB')
    return redirect("blockStudent")

@superuser_required
def applyUnblockAll(req):
    Student.objects.all().update(status='N')
    return redirect("blockStudent")

@superuser_required
def addJob(request):
    branches=Branch.objects.all()
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save()
            selected_branches = request.POST.getlist('allowed_branches')
            print(selected_branches)
            for branch_id in selected_branches:
                branch = Branch.objects.get(id=branch_id)
                job_branch = Job_branch.objects.create(job=job, branch=branch)
                job_branch.save()
            job.save()
            messages.success(request, f"{job.title} added successfully!")
            return redirect('jobs')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = JobForm()
    
    context = {'form': form,"branches":branches}
    return render(request, "administrator/company/addjob.html", context)

@superuser_required
def companies(request):
    companies=Company.objects.all()
    if request.method == 'POST':
        form = CompanyForm(request.POST,request.FILES)
        if form.is_valid():
            companynew = form.save()
            messages.success(request,message=" {0} added Successfully!".format(companynew))
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    messages.error(request, message=f"{field} : {error}")
            return redirect('admin')
    else:
        form = CompanyForm()
    return render(request, "administrator/company/companies.html",{'companies':companies})

@staff_required
def jobs(request):
    Job.objects.filter(registration_last_date__lt=datetime.now(timezone.utc)).update(reg_open=False)
    jobs=Job.objects.all()
    context={
        'jobs':jobs
    }
    return render(request, "administrator/company/jobs.html",context)


@superuser_required
def deletecompany(request,id):
    c=get_object_or_404(Company,id=id)
    cname=c.c_name
    c.delete()
    messages.success(request, message=" {0} deleted Successfully!".format(cname))
    return redirect('companies')

@superuser_required
def editCompany(request,id):
    company=get_object_or_404(Company,id=id)
    cname=company.c_name
    if request.method == 'GET':
        form=CompanyForm(instance=company)
        context={
            'form':form,
            'company':company
        }
        return render(request,"administrator/company/editCompany.html",context)
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

@superuser_required
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
            user = User.objects.filter(username=username).first()
            if user:
                user.set_password(new_password)
                user.save()
                messages.success(request, f'Password updated successfully for user {username}')
            else:
                messages.error(request, f'{username} username doesnt exist')
            return redirect('changePasswordAdmin')

    return render(request, 'administrator/student/changePasswordAdmin.html')


@superuser_required
def addNewsUpdates(request):
    form=NewsForm()
    if request.method=='POST':
        form=NewsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Added successfully.')
            return redirect('/au/newsAndUpdates')
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    messages.error(request, message=f"{field} : {error}")
    context={'news':form}
    return render(request,"administrator/add_newsUpdates.html",context)


@staff_required
def newsAndUpdates(request):
    news=Notice.objects.all().order_by('-updated_on')
    return render(request,'administrator/newsAndUpdates.html',{'news':news})

@superuser_required
def updateNews(request,id):
    notice=Notice.objects.get(id=id)
    form=NewsForm(instance=notice)
    if request.method=='POST':
        form=NewsForm(request.POST,instance=notice)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated successfully.')
            return redirect('/au/newsAndUpdates')
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    messages.error(request, message=f"{field} : {error}")
    context={'news':form}
    return render(request,'administrator/updateNews.html',context)


@superuser_required
def deleteNews(request,id):
    notice=get_object_or_404(klass=Notice,id=id)
    notice.delete()
    messages.success(request, 'Deleted successfully.')
    return redirect('../../newsAndUpdates')


@superuser_required
def deleteStaff(request,uname):
    staff=get_object_or_404(User,username=uname)
    staff.delete()
    messages.success(request, message="Deleted staff successfully")
    return redirect("manageportal")
   
@superuser_required
def adminEditor(request):
    if request.method=='POST' and  request.FILES.get('slider_image') :
        form = SliderForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, message="Image added successfully")
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    messages.error(request, message=f"{field} : {error}")
    elif request.method=='POST' and request.POST.get('rule') :
        form = RuleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, message="Rule added successfully")
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    messages.error(request, message=f"{field} : {error}")
    elif request.method=='POST' and request.FILES.get('image'):
        form = GalleryForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, message="Added to gallery successfully")
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
    
    galleryForm=GalleryForm()
    sliderForm=SliderForm()
    teamForm=TeamForm()
    ruleForm=RuleForm()
    gallery=Gallery.objects.all()
    members = Team.objects.all()
    sliders = Slider.objects.all()
    rules=Rule.objects.all()
    return render(request, "administrator/adminEditor.html",context={'members':members,'sliders':sliders,'rules':rules,'sliderForm':sliderForm,'teamForm':teamForm,'ruleForm':ruleForm,'galleryForm':galleryForm,'gallery':gallery})

@superuser_required
def blockStudent(request):
    students = Student.objects.all().order_by('-updated_at')[:5]
    return render(request,"administrator/blockStudent.html",{'students':students})



@superuser_required
def profileEditBlock(request,id):
    user=User.objects.get(id=id)
    student=Student.objects.get(user=user)
    student.editable = student.editable == False
    student.save()
    return redirect("blockStudent")

@superuser_required
def profileEditBlockAll(req):
    Student.objects.all().update(editable=False)
    return redirect("blockStudent")

@superuser_required
def profileEditUnblockAll(req):
    Student.objects.all().update(editable=True)
    return redirect("blockStudent")

@superuser_required
def deleteTeamMember(request,id):
    teamobj=get_object_or_404(Team,id=id)
    teamobj.delete()
    messages.success(request, message="Member deleted successfully")
    return redirect('/au/adminEditor')

@superuser_required
def editTeamMember(request,id):
    teamobj=get_object_or_404(Team,id=id)
    if request.method=="POST":
        form=TeamForm(request.POST,request.FILES,instance=teamobj)
        if form.is_valid():
            form.save()
            memname=teamobj.mem_name
            messages.success(request, message="{0} Edited successfully".format(memname))
            return redirect(to='/au/adminEditor')
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    messages.error(request, message=f"{field} : {error}")

    form=TeamForm(instance=teamobj)
    return render(request, "administrator/editTeamMember.html",context={'form':form,'member':teamobj})

@superuser_required
def editGallery(request,id):
    gobj=get_object_or_404(Gallery,id=id)
    if request.method=="POST":
        form=GalleryForm(request.POST,request.FILES,instance=gobj)
        if form.is_valid():
            form.save()
            title=gobj.title
            messages.success(request, message="{0} Edited successfully".format(title))
            return redirect(to='/au/adminEditor')
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    messages.error(request, message=f"{field} : {error}")
    form = GalleryForm(instance=gobj)
    return render(request, "administrator/editGallery.html",context={'form':form,'image':gobj})

@superuser_required
def deleteSlider(request,id):
    slidobj = get_object_or_404(Slider,id=id)
    slidobj.delete()
    messages.success(request, message="Slider image deleted successfully")
    return redirect('/au/adminEditor')

@superuser_required
def editRule(request,id):
    rule=get_object_or_404(klass=Rule,id=id)
    form=RuleForm(instance=rule)
    if request.POST:
        form=RuleForm(request.POST,instance=rule)
        if form.is_valid():
            form.save()
            messages.success(request, message="Rule Edited successfully")
            return redirect(to="/au/adminEditor")
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    messages.error(request, message=f"{field} : {error}")
    return render(request, template_name="administrator/editRule.html",context={'form':form})

@superuser_required
def deleteRule(request,id):
    rule=get_object_or_404(klass=Rule,id=id)
    rule.delete()
    messages.success(request, message="Deleted successfully")
    return redirect(to="/au/adminEditor")

@superuser_required
def deletegimage(request,id):
    g_img=get_object_or_404(Gallery,id=id)
    title=g_img.title
    g_img.delete()
    messages.success(request, message="{0} deleted successfully".format(title))
    return redirect(to="/au/adminEditor")

@staff_required
def registerHome(request):
    years=YearBatch.objects.all()
    selected={'id':-1}
        
    students = zip([],[])
    if request.method=="POST" and request.POST.get("year"):
        selectedYear=int(request.POST.get("year"))
        selectedYear=get_object_or_404(YearBatch,pk=selectedYear)
    else:
        selectedYear=YearBatch.objects.all().order_by('-endYear').first()

    jobs=Job.objects.filter(yearBatch=selectedYear)
    return render(request,"administrator/report/registerList.html",context={'heads':heads,'jobs':jobs,'students':students,'selected':selected,'years':years,'selectedYear':selectedYear,})

@staff_required
def registerList(request,id):
    students=[]
    pjs=[]
    selected={'id':id}
    years=YearBatch.objects.all()
    if request.GET.get("year"):
        try:
            selectedYear=YearBatch.objects.filter(pk=int(request.GET.get("year"))).first()
        except:
            pass
    if not selectedYear:
        selectedYear=YearBatch.objects.all().order_by('-endYear').first()

    if id==0:
        jobSt=Job_student.objects.filter(job__yearBatch=selectedYear).select_related('student','student__user')
        selected['job']='ALL'
    else:
        job=get_object_or_404(Job,id=id)
        jobSt=Job_student.objects.filter(job=job).select_related('student','student__user')
        selected['job']=str(job)
    for j in jobSt:
        students.append(j.student)
        pjs.append(PreviousJob.objects.filter(user=j.student.user))
        
    stLen=len(students)
    students = zip(students, pjs)
    jobs=Job.objects.filter(yearBatch=selectedYear)
    return render(request,"administrator/report/registerList.html",context={'heads':heads,'jobs':jobs,'students':students,'selected':selected,'years':years,'selectedYear':selectedYear,'stLen':stLen})
    
@staff_required
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

@staff_required
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
    
@staff_required
def viewJob(request,id):
    job=get_object_or_404(Job,id=id)
    if job.reg_open==True and job.registration_last_date<datetime.now(timezone.utc):
        job.reg_open=False
        job.save()
    context={
        'job':job
    }
    return render(request,"administrator/company/viewJob.html",context)

@superuser_required
def deleteJob(request, id):
    job_code = get_object_or_404(Job, id=id)
    if request.method == 'POST':
            job_code.delete()
            messages.success(request, ' deleted successfully.')
    else:
            messages.warning(request, 'Cannot delete')
    return redirect('jobs')

@superuser_required
def editJob(request,id):
    job=get_object_or_404(Job,id=id)
    branches=Branch.objects.all()
    job_branches = Job_branch.objects.filter(job=job)
    associated_branches = list(job_branches.values_list('branch_id', flat=True))
    print(associated_branches)
    jobname=job.title
    if request.method=='POST':
        form = JobForm(request.POST,instance=job)
        updated_branches = request.POST.getlist('allowed_branches')
        Job_branch.objects.filter(job=job).delete()
        for branch_id in updated_branches:
            branch = Branch.objects.get(id=branch_id)
            Job_branch.objects.create(job=job, branch=branch)
        if form.is_valid():
            form.save()
            messages.success(request, message=" {0} updated Successfully!".format(jobname))
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    messages.error(request, message=f"{field} : {error}")
    else:
        form=JobForm(instance=job)
        context={
            'form':form,
            'branches':branches,
            'associated_branches':associated_branches
        }
        return render(request,"administrator/company/editJob.html",context)
    return redirect('viewJob', id=job.id)

@staff_required
def search(request):
    recently_logged_in_users = User.objects.filter(last_login__isnull=False).exclude(is_staff=True).order_by('-last_login')[:10]
    students=[]
    for user in recently_logged_in_users:
        student = get_object_or_404(Student,user=user)
        if student:
            students.append(student)
    return render(request,"administrator/search.html",{'students':students})

@staff_required
def viewprofile(request,id):
    user=get_object_or_404(User,id=id)
    student=get_object_or_404(Student,user=user)
    return render(request,"administrator/student/viewprofile.html",{'student':student})

@staff_required
def manageSelections(request):
    years=YearBatch.objects.all()


    selectedYear=False
    if request.GET.get("year"):
        try:
            selectedYear=YearBatch.objects.filter(pk=int(request.GET.get("year"))).first()
        except:
            pass

    if not selectedYear:
        selectedYear=YearBatch.objects.all().order_by('-endYear').first()

    jobs=Job.objects.filter(yearBatch=selectedYear)

    selectedJob=False
    if request.GET.get("job"):
        try:
            selectedJob=Job.objects.filter(pk=int(request.GET.get("job")),yearBatch=selectedYear).first()
        except:
            pass

    if not selectedYear:
        selectedYear=Job.objects.filter(yearBatch=selectedYear).first()


    jobSt=Job_student.objects.filter(job=selectedJob)
    appliedStudents=Job_student.objects.filter(status=Job_student.Status.APPLIED)
    offeredStudents=Job_student.objects.filter(status=Job_student.Status.OFFERED)
    placedStudents=Job_student.objects.filter(status=Job_student.Status.PLACED)
    rejectedStudents=Job_student.objects.filter(status=Job_student.Status.REJECTED)
    studentsPlacedCount = placedStudents.count() if placedStudents else 0
    studentsOfferedCount = offeredStudents.count() if offeredStudents else 0
    studentsAppliedCount = appliedStudents.count() if appliedStudents else 0
    studentsRejectedCount = rejectedStudents.count() if rejectedStudents else 0
    return render(request,"administrator/manageSelections.html",context={'job_students':jobSt,'selectedYear':selectedYear,'years':years,'selectedJob':selectedJob,'jobs':jobs,'appliedStudents':studentsAppliedCount,'offeredStudents':studentsOfferedCount,'placedStudents':studentsPlacedCount,'rejectedStudents':studentsRejectedCount})

@staff_required
def viewmanageSelections(request,id):
    student=get_object_or_404(Job_student,id=id)
    if request.method == 'POST':
        status=request.POST.get('status')
        if status == Job_student.Status.OFFERED or status == Job_student.Status.REJECTED or status == Job_student.Status.PLACED:
            student.status=status
        student.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@superuser_required
def resetportal(request):
    users = User.objects.exclude(is_superuser=True)
    users.delete()
    students=Student.objects.all()
    students.delete()
    jobs=Job.objects.all()
    jobs.delete()
    job_student=Job_student.objects.all()
    job_student.delete()
    companys=Company.objects.all()
    companys.delete()
    notices=Notice.objects.all()
    notices.delete()
    return redirect('admin')

@superuser_required
def manageportal(request):
    if request.method=='POST' and request.POST.get('startYear') :
        form = YearBatchForm(request.POST)
        if form.is_valid():
            year = form.save()
            messages.success(request, message=" {0}-{1} year added Successfully!".format(year.startYear,year.endYear))
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    messages.error(request, message=f"{field} : {error}")
    elif request.method=='POST' and request.POST.get('branchname1') :
        form = BranchForm(request.POST)
        if form.is_valid():
            branch=form.save()
            messages.success(request, message="Branch Combination {0}-{1} added successfully".format(branch.branchname1,branch.branchname2))
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    messages.error(request, message=f"{field} : {error}")
    elif request.method=='POST' and request.POST.get('username'):
        form=StaffForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(request.POST['password'])
            user.is_staff=True
            user.save()
            messages.success(request, message="Added staff successfully")
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    messages.error(request, message=f"{field} : {error} ")
    elif request.method=='POST' and request.POST.get('placed_count'):
        form=StatisticForm(request.POST,instance=statistic_obj)
        if form.is_valid():
            form.save()
            messages.success(request,message="Placement Stats Updated successfully")
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    messages.error(request, message=f"{field} : {error}")

    years=YearBatch.objects.all()
    branches=Branch.objects.all()
    staffs=User.objects.filter(is_staff=True,is_superuser=False)
    staffform=StaffForm()
    statsform=StatisticForm(instance=statistic_obj)
    return render(request,"administrator/portal/manage_portal.html",{'years':years,'branches':branches,'staffs':staffs,'staffform':staffform,'statsform':statsform})

@superuser_required
def deleteYearBatch(request, id):
    academic_batch = get_object_or_404(YearBatch, id=id)
    st=Student.objects.filter(yearBatch=academic_batch)
    for s in st:
        s.delete()
    academic_batch.delete()

    messages.success(request,message='{0}-{1} deleted successfully.'.format(academic_batch.startYear,academic_batch.endYear))
    return redirect('manageportal')

@superuser_required
def deleteBranch(request,id):
    branch=get_object_or_404(Branch,id=id)
    messages.success(request,message='{0}-{1} deleted successfully.'.format(branch.branchname1,branch.branchname2))
    branch.delete()
    return redirect('manageportal')
@staff_required
def companyList(request):
    heads=["Company","Job Title","CTC","Number of applications","Number of job offers","Number of placed Students"]
    years=YearBatch.objects.all()

    selectedYear=False
    if request.GET.get("year"):
        try:
            selectedYear=YearBatch.objects.filter(pk=int(request.GET.get("year"))).first()
        except:
            pass

    
    if not selectedYear:
        selectedYear=YearBatch.objects.all().order_by('-endYear').first()

    jobs=Job.objects.filter(yearBatch=selectedYear).annotate(applied=Count("job_student"),offered=Count("job_student",filter=Q(job_student__status=Job_student.Status.OFFERED)),placed=Count("job_student",filter=Q(job_student__status=Job_student.Status.PLACED)))

    return render(request,"administrator/report/companyList.html",context={'years':years,'selectedYear':selectedYear,'jobs':jobs,'heads':heads})
    

@staff_required
def student_report_list(request):
    heads=["USN","Name","CTC","Company","Job Role"]
    years=YearBatch.objects.all()

    selectedYear=False
    if request.GET.get("year"):
        try:
            selectedYear=YearBatch.objects.filter(pk=int(request.GET.get("year"))).first()
        except:
            pass
    
    if not selectedYear:
        selectedYear=YearBatch.objects.all().order_by('-endYear').first()

    students=Job_student.objects.filter(student__yearBatch=selectedYear,status=Job_student.Status.PLACED).select_related('student','job','student__user')
    return render(request,"administrator/report/studentReport.html",context={'years':years,'selectedYear':selectedYear,'students':students,'heads':heads})



@superuser_required
def yearbatch_stats(request):
    if request.method=='POST' and request.POST.get('year'):
        year=request.POST.get('year')
        jobs=Job.objects.filter(yearBatch=year)
        statistic_obj.placed_count=Job_student.objects.filter(student__yearBatch=year,job__in=jobs,status=Job_student.Status.PLACED).count()
        statistic_obj.offers_count=Job_student.objects.filter(student__yearBatch=year,job__in=jobs,status=Job_student.Status.OFFERED).count()
        statistic_obj.highest_ctc = Job.objects.filter(yearBatch=year).aggregate(max_ctc=Max('ctc_pa')).get('max_ctc', 0) or 0
        statistic_obj.avg_ctc = Job.objects.filter(yearBatch=year).aggregate(avg_ctc=Avg('ctc_pa')).get('avg_ctc', 0) or 0
        statistic_obj.companies_visited = jobs.filter(yearBatch=year).values('company').distinct().count()
        statistic_obj.save()
        messages.success(request,message="Placement Stats Updated successfully")
    
    return redirect('manageportal')

@superuser_required
def editBranch(request,id):
    branch=get_object_or_404(Branch,id=id)
    if request.method=='POST':
        form = BranchForm(request.POST,instance=branch)
        if form.is_valid():
            form.save()
            messages.success(request, message=" Branch updated Successfully!")
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    messages.error(request, message=f"{field} : {error}")
    else:
        form=BranchForm(instance=branch)
        context={
            'form':form
        }
        return render(request,"administrator/portal/editBranch.html",context)
    return redirect("manageportal")
    

