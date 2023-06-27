from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .forms import StudentForm,PreviousJobForm
from .models import Student,PreviousJob
from django.contrib.auth.decorators import login_required
from administrator.models import Job_branch, Notice,Job_student
from home.models import Company
from django.contrib import messages
from django.shortcuts import get_object_or_404
from home.models import Job
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.http import Http404
from django.utils.timezone import datetime,timezone
from home.models import  Rule

def normaluser_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
                return redirect(f'/login?next={request.path}')
        if request.user.is_staff:
            raise Http404
        return view_func(request, *args, **kwargs)
    return wrapped_view

def normaluserWithProfile_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f'/login?next={request.path}')
        if request.user.is_staff:
            raise Http404
        if request.user.student and not request.user.student.nameAadhar:
            messages.warning(request=request,message="Please fill your profile details")
            return redirect("/profile/update")
        return view_func(request, *args, **kwargs)
    return wrapped_view

@normaluser_required
def updateProfile(request):
    if request.user.is_superuser:
        return redirect('/au/')
    
    s=Student.objects.filter(user=request.user).first()
    pjs=PreviousJob.objects.filter(user=request.user)
    if request.method=="POST":
        form=StudentForm(request.POST,request.FILES,instance=s)
        if form.is_valid():
            st=form.save()
            messages.success(request, message="Profile updated successfully")
            return redirect('profile')
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    messages.error(request, message=f"{field} : {error}")

    form=StudentForm(instance=s)
    pjForm=PreviousJobForm()
    return render(request, "student/updateprofile.html",context={'form':form,'previousJobs':pjs,'pjForm':pjForm})


@normaluser_required
def addPreviousJob(request):
    if request.method=="POST":
        form=PreviousJobForm(request.POST)
        if form.is_valid():
            pj=form.save(commit=False)
            pj.user=request.user
            pj.save()
            messages.success(request, message="Added successfully")
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    messages.error(request, message=f"{field} : {error}")
    return redirect('/profile/update')

@normaluser_required
def deletePreviousJob(request,id):

    pj=get_object_or_404(PreviousJob,id=id)
    pj.delete()
    messages.success(request, message="Deleted successfully")
    return redirect('/profile/update')

@normaluser_required
def editPreviousJob(request,id):

    pj=get_object_or_404(PreviousJob,id=id)
    if request.method=="POST":
        form=PreviousJobForm(request.POST,instance=pj)
        if form.is_valid():
            form.save()
            messages.success(request, message="Edited successfully")
            return redirect(to='/profile/update')
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    messages.error(request, message=f"{field} : {error}")

    form=PreviousJobForm(instance=pj)
    return render(request, "student/editpreviousjob.html",context={'form':form})

@normaluserWithProfile_required
def registerCompany(request):
    student = Student.objects.get(user=request.user)
    Job.objects.filter(registration_last_date__lt=datetime.now(timezone.utc)).update(reg_open=False)
    jobs = Job.objects.filter(yearBatch=student.yearBatch)
    jobs_students = Job_student.objects.filter(student=request.user.student)
    total_companies =jobs.count()
    applied_companies = jobs_students.count()
    open_companies = jobs.filter(reg_open = True).count()
    closed_companies = jobs.filter(reg_open = False).count()
    return render(request, "student/registerCompany.html",{'jobs': jobs, 'jobs_students': jobs_students,'total_companies':total_companies,'applied_companies':applied_companies,'open_companies':open_companies,'closed_companies':closed_companies})

@normaluser_required
def changePassword(request):
    if request.method == 'POST':
        current_password = request.POST.get('password')
        new_password = request.POST.get('newpassword')
        confirm_password = request.POST.get('confirmpassword')
        
        if not request.user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('changePassword')
        
        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('changePassword')
        
        request.user.set_password(new_password)
        request.user.save()
        messages.success(request, 'Password changed successfully.')
        return redirect('changePassword')
        
    return render(request, 'student/changePassword.html')

@normaluserWithProfile_required
def student_home(request):
    news=Notice.objects.filter(hidden=False).order_by('-updated_on')
    return render(request,"student/student_home.html",{'news':news})

def is_eligible(job, student):
        student_branch = student.branch.id
        job_branches = Job_branch.objects.filter(job=job)
        job_student=Job_student.objects.filter(student=student,status=Job_student.Status.PLACED).first()

        if not student.name:
            return False,"Please fill profile details"
        if not student.branch:
            return False,"Please fill profile details"
        if student.status!=Student.Blocked.NOT_BLOCKED:
            return False,"Your profile is blocked from applying"
        if not job.reg_open:
            return False,"Registration closed"
        if student_branch not in job_branches.values_list('branch', flat=True):
            return False,"Your branch is not eligible"
        if job_student:
            return False,"You are already placed in "+str(job_student.job)
        if student.cgpa < job.curr_cgpa:
            return False,"Cgpa is low"
        if student.tenPercentage < job.sslc:
            return False,"10th percentage low"
        if student.twelvePercentage < job.puc and student.diplomaPercentage < job.diploma:
            return False,"12th percentage low"
        if student.degreePercentage < job.degree:
            return False,"Degree percentage low"
        if student.diplomaPercentage < job.diploma:
            return False,"Diploma percentage low"
        if student.activeBacklog > job.max_activebacklog:
            return False,"Active backlogs are more"
        if student.totalBacklog > job.max_histbacklog:
            return False,"Total backlogs are more"
        if student.gap_edu > job.gap_edu:
            return False,"Gap is eduction is more"
        if job.min_dob and (not student.dateOfBirth or student.dateOfBirth < job.min_dob):
            return False,"Date of birth out of range"
        if job.max_dob and (not student.dateOfBirth or student.dateOfBirth > job.max_dob):
            return False,"Date of birth out of range"
        if student.yearBatch != job.yearBatch:
            return False,"Job not applicable for your academic year"

        return True,""

@normaluserWithProfile_required
def companyPage(request,id):
    job = get_object_or_404(Job,id=id)
    job_branches=Job_branch.objects.filter(job=job)
    if job.reg_open==True and job.registration_last_date<datetime.now(timezone.utc):
        job.reg_open=False
        job.save()
    student = request.user.student
    eligible,reason = is_eligible(job,student)
    job_student = Job_student.objects.filter(job=job,student=student).first()

    if request.method == 'POST' and eligible:
            if not job_student:
                job_student = Job_student.objects.create(job=job,student=request.user.student)
                job_student.save()
                messages.success(request, 'Applied successfully.')
            else:
                messages.error(request, 'Already applied.')
            return redirect('companyPage',id=id)

    return render(request,"student/companyPage.html",{'job':job,'id':id,'student':student,'eligible':eligible,'job_student':job_student,'job_branches':job_branches,'reason':reason})

@normaluser_required
def rules(request):
    srules = Rule.objects.all()
    return render(request, "student/rules.html",context={'srules':srules})

@normaluserWithProfile_required
def profile(request):
    return render(request, "student/profile.html")