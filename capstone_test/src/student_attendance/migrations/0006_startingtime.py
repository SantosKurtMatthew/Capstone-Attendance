# Generated by Django 4.1.5 on 2023-02-01 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_attendance', '0005_rename_dailyintegers_dailyinteger'),
    ]

    operations = [
        migrations.CreateModel(
            name='StartingTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.IntegerField(default=0)),
                ('startinghour', models.IntegerField(default=7)),
                ('startingminute', models.IntegerField(default=0)),
            ],
        ),
    ]