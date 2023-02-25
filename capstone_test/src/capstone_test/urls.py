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

from student_attendance.views import attendancecode_view, attendancesubmit_view, studentdatabase_view, newstudent_view, navbar_view, attendancetoday_view, deletestudent_view, accountcreate_view, login_view, logout_view, instructions_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', attendancesubmit_view, name='attendance_submit'),
    #path('submit/', attendancesubmit_view, name='attendance_submit'),
    path('attendance/', attendancecode_view, name='attendance_code'),
    path('database/', studentdatabase_view, name='student_database'),
    path('navbar/', navbar_view, name='nav-bar'),
    path('today/', attendancetoday_view, name='today_attendance'),
    path('newstudent/', newstudent_view, name='new_studentinfo'),
    path('deletestudent/', deletestudent_view, name='delete_studentinfo'),
    path('newaccount/', accountcreate_view, name='new_account'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('instructions/', instructions_view, name='instructions'),
]
