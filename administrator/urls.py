from django.urls import path
from . import views
urlpatterns=[
path('au/',views.index, name='admin'),   
path('au/student/add',views.addStudent, name='addStudent'),  
path('au/adminEditor',views.adminEditor,name='adminEditor'), 
]