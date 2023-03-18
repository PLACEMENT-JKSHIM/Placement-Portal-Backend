from django.forms import ModelForm
from django import forms
from .models import Student,PreviousJob

always_enabled_list=['image','resume','pastExperience','projects','preferredJobLocation']
class StudentForm(ModelForm):
    def __init__(self,*args,**kwargs):
        super(StudentForm, self).__init__(*args,**kwargs)
        if self.instance and not self.instance.editable:
            for i in self.fields:
                if i not in always_enabled_list:
                    self.fields[i].disabled=True

    class Meta:
        model=Student
        exclude=('user','status','editable')

        widgets=   {
            'dateOfBirth': forms.DateInput(attrs={'type': 'date'}),
        }
        
        
class PreviousJobForm(ModelForm):
    class Meta:
        model=PreviousJob
        fields=['role','yearsofExperience','monthsofExperience','company']