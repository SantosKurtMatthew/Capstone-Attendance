# Generated by Django 4.1.7 on 2023-04-15 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_attendance', '0013_students_attendancesubmit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancesubmit',
            name='submit_time',
            field=models.TimeField(auto_now=True),
        ),
    ]
