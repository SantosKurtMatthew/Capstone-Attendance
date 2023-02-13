from django.contrib import admin

# Register your models here.
from .models import AttendanceSubmit, Students, DailyInteger, StartingTime, TeacherPasswords

admin.site.register(AttendanceSubmit)
admin.site.register(Students)
admin.site.register(DailyInteger)
admin.site.register(StartingTime)


