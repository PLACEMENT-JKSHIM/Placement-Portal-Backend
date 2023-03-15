from django.forms import ModelForm 
from django.contrib.auth.models import User

from home.models import Slider, Team

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
