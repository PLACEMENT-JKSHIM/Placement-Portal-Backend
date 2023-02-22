from django.urls import path
from . import views
urlpatterns=[
path('',views.index, name='index'),   
path('login',views.login,name="login"),
path('home',views.home,name="home"),
path('gallery',views.gallery,name="gallery"),
<<<<<<< HEAD
path('profile',views.profile,name="profile"),
=======
path('student/changePassword',views.changePassword,name="changePassword")
>>>>>>> d4d531d09a0217949bf09801434b5a1dd79b97c3
]