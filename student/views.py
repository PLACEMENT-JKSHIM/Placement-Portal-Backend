from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .forms import StudentForm,PreviousJobForm
from .models import Student,PreviousJob
from django.contrib.auth.decorators import login_required
from administrator.models import Notice,Job_student
from django.contrib import messages
from django.shortcuts import get_object_or_404
from home.models import Job
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.http import Http404


def normaluser_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f'/login?next={request.path}')
        if request.user.is_superuser:
            raise Http404
        return view_func(request, *args, **kwargs)
    return wrapped_view

@normaluser_required
def updateProfile(request):
    if request.user.is_superuser:
        return redirect('/au/')
    
    s=Student.objects.filter(user=request.user).first()
    pjs=PreviousJob.objects.filter(user=request.user)
    if request.method=="POST":
        print(request.FILES)
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

@normaluser_required
def registerCompany(request):
    jobs = Job.objects.all()
    jobs_students = Job_student.objects.filter(student=request.user.student)
    return render(request, "student/registerCompany.html",{'jobs': jobs, 'jobs_students': jobs_students})

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

@normaluser_required
def student_home(request):
    news=Notice.objects.filter(hidden=False).order_by('-updated_on')
    return render(request,"student/student_home.html",{'news':news})

def is_eligible(job, student):
        if not student.name:
            return False
        if student.cgpa < job.curr_cgpa:
            return False
        if student.tenPercentage < job.sslc:
            return False
        if student.twelvePercentage < job.puc:
            return False
        # elif self.student.diplomaPercentage < self.job.diploma:

        # return False
        if student.degreePercentage < job.degree:
            return False
        if student.activeBacklog > job.max_activebacklog:
            return False
        if student.totalBacklog > job.max_histbacklog:
            return False
        # if self.student.gap_edu > self.job.gap_edu:
        #     return False
        if not student.dateOfBirth or student.dateOfBirth < job.min_dob:
            return False
        if not student.dateOfBirth or student.dateOfBirth > job.max_dob:
            return False
        return True

@normaluser_required
def companyPage(request,id):
    job = get_object_or_404(Job,id=id)
    student = request.user.student
    eligible = is_eligible(job,student)
    job_student = Job_student.objects.filter(job=job,student=student).first()

    if request.method == 'POST' and eligible:
            if not job_student:
                job_student = Job_student.objects.create(job=job,student=request.user.student)
                job_student.save()
                messages.success(request, 'Applied successfully.')
            else:
                messages.error(request, 'Already applied.')
            return redirect('companyPage',id=id)

    return render(request,"student/companyPage.html",{'job':job,'id':id,'student':student,'eligible':eligible,'job_student':job_student})