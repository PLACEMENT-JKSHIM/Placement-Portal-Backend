from django.urls import path
from . import views

urlpatterns=[
path('',views.index, name='index'),   
path('login',views.login,name="login"),
path('gallery',views.gallery,name="gallery"),
path('rules',views.rules,name="rules"),
path('profile',views.profile,name="profile"),
path('logout',views.logout, name='logout'), 
]