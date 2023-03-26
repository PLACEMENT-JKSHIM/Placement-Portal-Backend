from django.forms import ModelForm 
from django.contrib.auth.models import User
from django import forms
from home.models import Slider, Team,Job,Company

class UserForm(ModelForm):
    class Meta:
        model=User
        fields=['username','password']

class SliderForm(ModelForm):
    class Meta:
        model = Slider
        fields = ['slider_image']

class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ['mem_name','mem_designation','mem_image','mem_description']

class JobForm(ModelForm):
    class Meta:

        model = Job
        fields = '__all__'
        widgets = {

            'min_dob': forms.DateInput(attrs={'type': 'date'}),

            'max_dob': forms.DateInput(attrs={'type': 'date'}),

            'talk_date': forms.DateInput(attrs={'type': 'date'}),

            'registration_date': forms.DateInput(attrs={'type': 'date'}),

            'interview_date': forms.DateInput(attrs={'type': 'date'}),

            'test_date': forms.DateInput(attrs={'type': 'date'}),

        }

class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ['c_name','about','image']
