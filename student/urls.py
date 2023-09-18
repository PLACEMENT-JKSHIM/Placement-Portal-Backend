from django.urls import path
from . import views
urlpatterns=[
path('profile/update',views.updateProfile, name='updateProfile'),   
path('previousjob/add',views.addPreviousJob, name='addPreviousJob'),   
path('previousjob/delete/<int:id>',views.deletePreviousJob, name='deletePreviousJob'), 
path('previousjob/edit/<int:id>',views.editPreviousJob, name='editPreviousJob') ,  
path('registerCompany',views.registerCompany,name="registerCompany"),
path('changePassword',views.changePassword,name="changePS"),
path('home',views.student_home,name='home'),  
path('company/<int:id>',views.companyPage,name='companyPage'),
path('rules',views.rules,name="rules"),
path('profile',views.profile,name="profile"),
]