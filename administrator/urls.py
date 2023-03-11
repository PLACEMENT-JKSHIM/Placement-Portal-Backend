from django.urls import path
from . import views
urlpatterns=[
path('au/',views.index, name='admin'),   
]