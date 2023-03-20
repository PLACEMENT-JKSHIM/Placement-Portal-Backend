from django.urls import path
from . import views
urlpatterns=[
path('profile/update',views.updateProfile, name='updateProfile'),   
path('previousjob/add',views.addPreviousJob, name='addPreviousJob'),   
path('previousjob/delete/<int:id>',views.deletePreviousJob, name='deletePreviousJob'), 
path('previousjob/edit/<int:id>',views.editPreviousJob, name='editPreviousJob') ,  
path('student/registerCompany',views.registerCompany,name="registerCompany"),
path('student_home',views.student_home,name='student_home'),  
]