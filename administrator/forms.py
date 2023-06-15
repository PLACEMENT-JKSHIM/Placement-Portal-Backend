from django.forms import ModelForm 
from django.contrib.auth.models import User
from django import forms
from home.models import Slider, Team,Job,Company,Rule,Gallery
from administrator.models import Notice
from student.models import Student,Branch
from home.models import YearBatch

class UserForm(ModelForm):
    yearBatch=forms.ModelChoiceField(queryset=YearBatch.objects.all())
    def __init__(self,*args,**kwargs):
        super(UserForm,self).__init__(*args,**kwargs)
        y=YearBatch.objects.all().order_by("-endYear").first()
        if y:
            self.fields['yearBatch'].initial=y.pk
    class Meta:
        model=User
        fields=['username','password']

class StaffForm(ModelForm):
    class Meta:
        model=User
        fields=['username','password']

class RuleForm(ModelForm):
    class Meta:
        model=Rule
        fields='__all__'

class SliderForm(ModelForm):
    class Meta:
        model = Slider
        fields = ['slider_image']

class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ['mem_name','mem_designation','mem_image','mem_description']

class JobForm(ModelForm):

    def __init__(self,*args,**kwargs):
        super(JobForm,self).__init__(*args,**kwargs)
        y=YearBatch.objects.all().order_by("-endYear").first()
        if y:
            self.fields['yearBatch'].initial=y.pk
    class Meta:

        model = Job
        fields = '__all__'
        widgets = {

            'min_dob': forms.DateInput(attrs={'type': 'date'}),

            'max_dob': forms.DateInput(attrs={'type': 'date'}),

            'talk_date': forms.DateInput(attrs={'type': 'date'}),

            'registration_last_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),

            'interview_date': forms.DateInput(attrs={'type': 'date'}),

            'test_date': forms.DateInput(attrs={'type': 'date'}),
        }

class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ['c_name','about','image']

class NewsForm(ModelForm):
    class Meta:
        model=Notice
        fields='__all__'


class GalleryForm(ModelForm):
    class Meta:
        model=Gallery
        fields='__all__'

class UpdateMarksForm(ModelForm):

    
    def __init__(self,*args,**kwargs):
        super(UpdateMarksForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].required=False

    usn=forms.CharField(max_length=150)


    class Meta:
        model=Student
        fields=['sgpa1','sgpa2','sgpa3','sgpa4','cgpa']
        widgets={
            'sgpa1':forms.NumberInput(attrs={'value':None,'min':0,'max':10,'required':False}),
            'sgpa2':forms.NumberInput(attrs={'value':None,'min':0,'max':10,'required':False}),
            'sgpa3':forms.NumberInput(attrs={'value':None,'min':0,'max':10,'required':False}),
            'sgpa4':forms.NumberInput(attrs={'value':None,'min':0,'max':10,'required':False}),
            'cgpa':forms.NumberInput(attrs={'value':None,'min':0,'max':10,'required':False}),
        }

    def clean(self):
        cleaned_data=super().clean()
        for field in self.Meta().fields:
            if cleaned_data[field]==None:
                cleaned_data[field]=getattr(self.instance, field)

        return cleaned_data

    def save(self,commit=True):
        instance=super().save(commit=False)
        instance.__dict__.update(self.cleaned_data)
        print(instance)
        if commit:
            instance.save()
        return instance

class YearBatchForm(ModelForm):
    class Meta:
        model=YearBatch
        fields='__all__'

class BranchForm(ModelForm):
    class Meta:
        model=Branch
        fields='__all__'