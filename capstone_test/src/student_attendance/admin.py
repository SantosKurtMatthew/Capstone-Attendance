from django.contrib import admin

# Register your models here.
from .models import Attendance, Students, DailyInteger, StartingTime

admin.site.register(Attendance)
admin.site.register(Students)
admin.site.register(DailyInteger)
admin.site.register(StartingTime)

