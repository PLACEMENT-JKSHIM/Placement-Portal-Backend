from django.forms import ModelForm,DateTimeInput,DateInput
from django.contrib.auth.models import User

from home.models import Slider, Team,Job

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
            'min_dob': DateTimeInput(attrs={'type': 'date'}),
            'max_dob': DateTimeInput(attrs={'type': 'date'}),
            'talk_date': DateInput(attrs={'type': 'date'}),
            'interview_date': DateInput(attrs={'type': 'date'}),
            'test_date': DateInput(attrs={'type': 'date'}),
        }