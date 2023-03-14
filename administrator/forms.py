from django.forms import ModelForm 
from django.contrib.auth.models import User

from home.models import Slider

class UserForm(ModelForm):
    class Meta:
        model=User
        fields=['username','password']

class SliderForm(ModelForm):
    class Meta:
        model = Slider
        fields = ['slider_image']
