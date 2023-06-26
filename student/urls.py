from django.urls import path
from . import views
urlpatterns=[
path('profile/update',views.updateProfile, name='updateProfile'),   
path('previousjob/add',views.addPreviousJob, name='addPreviousJob'),   
path('previousjob/delete/<int:id>',views.deletePreviousJob, name='deletePreviousJob'), 
path('previousjob/edit/<int:id>',views.editPreviousJob, name='editPreviousJob') ,  
path('student/registerCompany',views.registerCompany,name="registerCompany"),
path('student/changePassword',views.changePassword,name="changePassword"),
path('home',views.student_home,name='home'),  
path('student/companyPage/<int:id>',views.companyPage,name='companyPage'),
path('rules',views.rules,name="rules"),
path('profile',views.profile,name="profile"),
]