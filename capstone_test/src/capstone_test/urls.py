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

from student_attendance.views import homepage_view, attendancecode_view, attendancesubmit_view, studentdatabase_view, newstudent_view, navbar_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage_view, name="homepage"),
    path('submit/', attendancesubmit_view, name='attendance_submit'),
    path('attendance/', attendancecode_view, name='attendance_code'),
    path('database/', studentdatabase_view, name='student_database'),
    path('newstudent/', newstudent_view, name='new_studentinfo'),
    path('navbar/', navbar_view, name='nav-bar')
]
