from django.contrib import admin

# Register your models here.
from .models import AttendanceSubmit, Students, DailyInteger, StartingTime, SectionList
from .resources import StudentResource
from import_export.admin import ImportExportModelAdmin


class StudentAdmin(ImportExportModelAdmin):
    resource_classes = [StudentResource]

admin.site.register(AttendanceSubmit)
admin.site.register(Students, StudentAdmin)
admin.site.register(DailyInteger)
admin.site.register(StartingTime)
admin.site.register(SectionList)


