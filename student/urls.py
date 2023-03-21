from django.urls import path
from . import views
urlpatterns=[
path('logoutStudent',views.logoutStudent, name='logoutStudent'),   
path('profile/update',views.updateProfile, name='updateProfile'),   
path('previousjob/add',views.addPreviousJob, name='addPreviousJob'),   
path('previousjob/delete/<int:id>',views.deletePreviousJob, name='deletePreviousJob'), 
path('previousjob/edit/<int:id>',views.editPreviousJob, name='editPreviousJob') ,  
path('student/registerCompany',views.registerCompany,name="registerCompany"),
path('student/changePassword',views.changePassword,name="changePassword"),
path('student_home',views.student_home,name='student_home'),  
]