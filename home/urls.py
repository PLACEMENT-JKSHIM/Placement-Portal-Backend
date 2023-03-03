from django.urls import path
from . import views
urlpatterns=[
path('',views.index, name='index'),   
path('login',views.login,name="login"),
path('home',views.home,name="home"),
path('gallery',views.gallery,name="gallery"),
path('rules',views.rules,name="rules"),
path('profile',views.profile,name="profile"),
path('student/changePassword',views.changePassword,name="changePassword"),
path('company',views.company,name="company"),
]