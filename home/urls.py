from django.urls import path
from . import views
urlpatterns=[
path('',views.index, name='index'),   
path('login',views.login,name="login"),
path('student_home',views.student_home,name="student_home"),
path('gallery',views.gallery,name="gallery"),
path('rules',views.rules,name="rules")
]