from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .forms import StudentForm,PreviousJobForm
from .models import Student,PreviousJob
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from home.models import Job

@login_required(login_url='/login')
def updateProfile(request):
    if request.user.is_superuser:
        return redirect('/au/')
    
    s=Student.objects.filter(user=request.user).first()
    pjs=PreviousJob.objects.filter(user=request.user)
    if request.method=="POST":
        form=StudentForm(request.POST,instance=s)
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

def registerCompany(request):
    jobs = Job.objects.all()
    return render(request, "student/registerCompany.html",{'jobs': jobs})