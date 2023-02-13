# Generated by Django 4.1.5 on 2023-02-02 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_attendance', '0009_students_sex_students_spr'),
    ]

    operations = [
        migrations.CreateModel(
            name='TodayAttendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('classnumber', models.IntegerField(default=0)),
                ('late', models.BooleanField()),
                ('absents', models.BooleanField()),
            ],
        ),
        migrations.RenameModel(
            old_name='Attendance',
            new_name='AttendanceSubmit',
        ),
    ]