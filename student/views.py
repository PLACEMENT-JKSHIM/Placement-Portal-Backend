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



@login_required(login_url='/login')
def logoutStudent(request):
    logout(request)
    return render(request,"home/index.html")

@login_required(login_url='/login')
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
            messages.success(request, message="Saved successfully")
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    messages.error(request, message=f"{field} : {error}")

    form=StudentForm(instance=s)
    pjForm=PreviousJobForm()
    return render(request, "student/updateprofile.html",context={'form':form,'previousJobs':pjs,'pjForm':pjForm})


@login_required(login_url='/login')
def addPreviousJob(request):
    if request.user.is_superuser:
        return redirect('/au/')

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

@login_required(login_url='/login')
def deletePreviousJob(request,id):
    if request.user.is_superuser:
        return redirect('/au/')

    pj=get_object_or_404(PreviousJob,id=id)
    pj.delete()
    messages.success(request, message="Deleted successfully")
    return redirect('/profile/update')

@login_required(login_url='/login')
def editPreviousJob(request,id):
    if request.user.is_superuser:
        return redirect('/au/')

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

@login_required
def registerCompany(request):
    jobs = Job.objects.all()
    jobs_students = Job_student.objects.filter(student=request.user.student)
    return render(request, "student/registerCompany.html",{'jobs': jobs, 'jobs_students': jobs_students})

@login_required
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

@login_required(login_url='/login')
def student_home(request):
    l1=Notice.objects.all();
    l2=sorted(l1,key=lambda x:x.updated_on, reverse=True);
    return render(request,"student/student_newsUpdates.html",{'news':l2})

@login_required(login_url='/login')
def companyPage(request,id):
    job = get_object_or_404(Job,id=id)
    if request.method == 'POST':
        if job_student.is_eligible():
            job_student = Job_student.create(job=job,student=request.user.student)
            job_student.status = 'A'
            job_student.save()
            messages.success(request, 'Applied successfully.')
            return redirect('companyPage',id=id)
        else:
            messages.error(request, 'You are not eligible for this job.')
            return redirect('companyPage',id=id)
    job_students = Job_student.objects.filter(job=job,student=request.user.student)
    return render(request,"student/companyPage.html",{'job':job,'job_students':job_students})