# Generated by Django 4.1.5 on 2023-02-01 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_attendance', '0006_startingtime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='startingtime',
            name='startinghour',
        ),
        migrations.RemoveField(
            model_name='startingtime',
            name='startingminute',
        ),
        migrations.AddField(
            model_name='startingtime',
            name='startTime',
            field=models.TimeField(default='7:00'),
        ),
    ]
