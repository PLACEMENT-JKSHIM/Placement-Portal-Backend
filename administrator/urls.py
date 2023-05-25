from django.urls import path
from . import views
urlpatterns=[
path('au/',views.index, name='admin'),   
path('au/reset',views.resetportal, name='resetportal'),
path('au/student/add',views.addStudent, name='addStudent'),
path('au/student/changePasswordAdmin',views.changePasswordAdmin, name='changePasswordAdmin'),
path('au/student/block',views.blockStudent,name='blockStudent'),
path('au/student/editBlock',views.editBlock,name='editBlock'),
path('au/company/addJob',views.addJob, name='addJob'),
path('au/company/viewJob/<int:id>',views.viewJob, name='viewJob'),
path('au/company/deleteJob/<int:id>',views.deleteJob, name='deleteJob'),
path('au/company/editJob/<int:id>',views.editJob, name='editJob'),
path('au/company/jobs',views.jobs, name='jobs'),
path('au/company/editCompany/<int:id>',views.editCompany,name='editCompany'),
path('au/company/companies',views.companies, name='companies'),
path('au/company/delete/<int:id>',views.deletecompany, name='deletecompany'), 
path('au/student/profileEditBlock/<int:id>/',views.profileEditBlock,name='profileEditBlock'),
path('au/student/profileEditUnblockAll',views.profileEditUnblockAll,name='profileEditUnblockAll'),
path('au/student/profileEditBlockAll',views.profileEditBlockAll,name='profileEditBlockAll'),
path('au/student/applyBlockEdit/<int:id>/',views.applyBlockEdit,name='applyBlockEdit'),
path('au/student/applyBlockAll',views.applyBlockAll,name='applyBlockAll'),
path('au/student/applyUnblockAll',views.applyUnblockAll,name='applyUnblockAll'),
path('au/student/loginBlockEdit/<int:id>/',views.loginBlockEdit,name='loginBlockEdit'),
path('au/student/loginBlockAll',views.LoginBlockAll,name='LoginBlockAll'),
path('au/student/loginUnBlockAll',views.LoginUnblockAll,name='LoginUnblockAll'),
path('au/student/search',views.search,name='search'),
path('au/student/profile/<int:id>',views.viewprofile,name='viewprofile'),
path('au/addNewsUpdates',views.addNewsUpdates,name='addNewsUpdates'), 
path('au/newsAndUpdates',views.newsAndUpdates,name='newsAndUpdates'), 
path('au/updateNews/<int:id>/',views.updateNews,name='updateNews'), 
path('au/deleteNews/<int:id>/',views.deleteNews,name='deleteNews'), 
path('au/adminEditor',views.adminEditor,name='adminEditor'),
path('au/adminEditor/deleteMember/<int:id>',views.deleteTeamMember, name='deleteTeamMember'),
path('au/adminEditor/editMember/<int:id>',views.editTeamMember, name='editTeamMember'),
path('au/adminEditor/deleteSlider/<int:id>',views.deleteSlider, name='deleteSlider'),
path('au/adminEditor/editGallery/<int:id>',views.editGallery, name='editGallery'),
path('au/adminEditor/deletegimage/<int:id>',views.deletegimage, name='deletegimage'),
path('au/registerlist',views.registerHome,name='registerHome'),
path('au/registerlist/resumes/<int:id>',views.downLoadResumes,name='downLoadResumes'),
path('au/registerlist/images/<int:id>',views.downLoadImages,name='downLoadImages'),
path('au/registerlist/<int:id>',views.registerList,name='registerList'),
path('au/rule/delete/<int:id>',views.deleteRule,name='deleteRule'),
path('au/rule/edit/<int:id>',views.editRule,name='editRule'),
path('au/student/update',views.updateStudent,name='updateStudent'),
path('au/student/update/usns',views.updateMultipleUsn,name='updateUsns'),
path('au/student/update/marks',views.updateMultipleMarks,name='updateMarks'),
path('au/addStaff',views.addStaff,name='addStaff'), 
path('au/deleteStaff/<str:uname>',views.deleteStaff,name='deleteStaff'), 
path('au/student/studentlist',views.studentList,name='studentList'),
path('au/student/studentlist/<int:id>',views.viewstudentList,name="viewstudentlist")
]