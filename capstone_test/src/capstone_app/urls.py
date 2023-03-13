"""capstone_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from student_attendance.views import (
    dailypassword_view, 
    attendancesubmit_view, 
    studentdatabase_view, 
    newstudent_view, 
    dailyattendance_view, 
    deletestudent_view, 
    accountcreate_view, 
    login_view, 
    logout_view, 
    instructions_view, 
    startingtimes_view, 
    dailyfunction_view, 
    purgedatabase_view, 
    passwordchange_view,
    exportpdf_view
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', attendancesubmit_view, name='attendance_submit'),
    path('instructions/', instructions_view, name='instructions'),
    path('dailyinteger/', dailypassword_view, name='attendance_code'),
    path('starttime/', startingtimes_view, name='starttime'),
    path('dailyattendance/', dailyattendance_view, name='today_attendance'),
    path('studentdatabase/', studentdatabase_view, name='student_database'),
    path('newstudent/', newstudent_view, name='new_studentinfo'),
    path('deletestudent/', deletestudent_view, name='delete_studentinfo'),
    path('newaccount/', accountcreate_view, name='new_account'),
    path('login/', login_view, name='login'),
    path('changepassword/', passwordchange_view, name='password_change'),
    #The urls without pages, only buttons
    path('logout/', logout_view, name='logout'),
    path('dailyfunction/', dailyfunction_view, name='dailyfunction'),
    path('purge/', purgedatabase_view, name='purgedb'),
    path('pdf/', exportpdf_view, name='exportpdf'),
]
