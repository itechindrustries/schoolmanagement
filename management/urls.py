from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('profile/', views.profile,name='profile'),
    path('change-password/', views.change_password,name='change-password'),
    path('logout/', views.logout_view,name='logout'),
    path('classes/', views.classes,name='classes'),
    path('student/', views.student,name='student'),
    path('attendance/', views.attendance,name='attendance'),
    path('attendance/add-attendance/', views.addattendance,name='add-attendance'),
    path('attendance/updateattendance/', views.updateattendance,name='updateattendance'),
    path('examarks/', views.examarks,name='examarks'),
    path('examarks/aexamarks/', views.aexamarks,name='aexamarks'),
    path('examarks/uexamarks/', views.uexamarks,name='uexamarks'),
    path('schedule/', views.schedule,name='schedule'),
    path('pushnotification/', views.pushnotification,name='pushnotification'),
    path('pushnotification/<pk>/delete/', views.delete_noti, name="delete_noti"),
    path('report-card/', views.report_card,name='report_card'),
    path('report-card/repo_result', views.repo_result,name='repo_result'),
]
