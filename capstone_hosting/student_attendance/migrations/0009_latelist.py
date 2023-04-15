# Generated by Django 4.1.7 on 2023-04-13 09:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student_attendance', '0008_alter_students_lrn'),
    ]

    operations = [
        migrations.CreateModel(
            name='LateList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latedate', models.DateField()),
                ('attendancesubmit', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='student_attendance.attendancesubmit')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_attendance.students')),
            ],
        ),
    ]
