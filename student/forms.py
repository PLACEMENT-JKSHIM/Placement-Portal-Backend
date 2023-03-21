from django.forms import ModelForm
from django import forms
from .models import Student,PreviousJob
from django.contrib.auth.models import User

always_enabled_list=['image','resume','pastExperience','projects','preferredJobLocation']
required_list=['name','nameAadhar','image','phoneNo','email','aadhar','pancard','dateOfBirth',
        'homeTown','homeState','address','preferredJobLocation','tenPercentage','tenBoard','tenPassYear','tenSchool','tenState','tenCountry',
        'mbaSpecialization','degreePercentage','degreeCourse','degreeCollege','degreePassYear','degreeState','degreeCountry','degreeCollege']

class StudentForm(ModelForm):
    def __init__(self,*args,**kwargs):
        super(StudentForm, self).__init__(*args,**kwargs)
        #commented code testing purpose
        # if self.instance:
        #     if self.instance.image:
        #         self.fields['image'].widget.attrs.update({'required':False})
        #     if self.instance.resume:
        #         self.fields['resume'].widget.attrs.update({'required':False})
        #     for i in self.fields:
        #         if i in required_list:
        #             self.fields[i].required=True
        if self.instance and not self.instance.editable:
            for i in self.fields:
                if i not in always_enabled_list:
                    self.fields[i].disabled=True
                    

    class Meta:
        model=Student
        exclude=('user','status','editable')

        widgets=   {
            'dateOfBirth': forms.DateInput(attrs={'type': 'date'}),
            'phoneNo': forms.NumberInput(attrs={'min': 1000000000,'max':99999999999}),
            'image': forms.FileInput(attrs={'accept': 'image/*','required':True}),
            'resume': forms.FileInput(attrs={'accept':'application/pdf','required':True}),
        }
        
        
class PreviousJobForm(ModelForm):
    class Meta:
        model=PreviousJob
        fields=['role','yearsofExperience','monthsofExperience','company']

class ChangePasswordForm(ModelForm):
    class Meta:
        model=User
        fields=['username','password']
