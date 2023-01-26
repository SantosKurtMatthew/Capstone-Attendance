from django.apps import AppConfig


class StudentAttendanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'student_attendance'

    def ready(self):
        from jobsfolder import updater
        updater.start()


    