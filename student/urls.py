from django.urls import path
from . import views
urlpatterns=[
path('profile/update',views.updateProfile, name='updateProfile'),   
path('previousjob/add',views.addPreviousJob, name='addPreviousJob'),   
path('previousjob/delete/<int:id>',views.deletePreviousJob, name='deletePreviousJob')   
]