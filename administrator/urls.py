from django.urls import path
from . import views
urlpatterns=[
path('au/',views.index, name='admin'),   
path('au/student/add',views.addStudent, name='addStudent'), 
path('au/student/block',views.blockStudent,name='blockStudent'),
path('au/student/editBlock',views.editBlock,name='editBlock'),
path('au/student/profileEditBlock/<int:id>/',views.profileEditBlock,name='profileEditBlock'),
path('au/student/profileEditUnblockAll',views.profileEditUnblockAll,name='profileEditUnblockAll'),
path('au/student/profileEditBlockAll',views.profileEditBlockAll,name='profileEditBlockAll'),
path('au/adminEditor',views.adminEditor,name='adminEditor'), 
]