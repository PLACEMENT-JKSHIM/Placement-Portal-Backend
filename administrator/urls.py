from django.urls import path
from . import views
urlpatterns=[
path('au/',views.index, name='admin'),   
path('au/student/add',views.addStudent, name='addStudent'),
path('au/student/changePasswordAdmin',views.changePasswordAdmin, name='changePasswordAdmin'),
path('au/student/block',views.blockStudent,name='blockStudent'),
path('au/student/editBlock',views.editBlock,name='editBlock'),
path('au/student/profileEditBlock/<int:id>/',views.profileEditBlock,name='profileEditBlock'),
path('au/student/profileEditUnblockAll',views.profileEditUnblockAll,name='profileEditUnblockAll'),
path('au/student/profileEditBlockAll',views.profileEditBlockAll,name='profileEditBlockAll'),
path('au/addNewsUpdates',views.addNewsUpdates,name='addNewsUpdates'), 
path('au/adminEditor',views.adminEditor,name='adminEditor'), 
path('au/adminEditor/deleteMember/<int:id>',views.deleteTeamMember, name='deleteTeamMember'),
path('au/adminEditor/deleteSlider/<int:id>',views.deleteSlider, name='deleteSlider'),
]