# Generated by Django 4.1.7 on 2023-03-13 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AttendanceSubmit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('password', models.IntegerField(default=0)),
                ('submit_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='DailyInteger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('integer', models.IntegerField(default=0)),
                ('creation_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='SectionList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.CharField(max_length=20)),
                ('highschool', models.CharField(default='shs', max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='StartingTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.IntegerField(default=0)),
                ('starttime', models.TimeField(default='7:00')),
            ],
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(default='', max_length=254)),
                ('grade', models.IntegerField(default=0)),
                ('section', models.CharField(default='', max_length=10)),
                ('classnumber', models.IntegerField(default=0)),
                ('lates', models.IntegerField(default=0)),
                ('absents', models.FloatField(default=0)),
                ('spr', models.IntegerField(default=0)),
                ('sex', models.CharField(blank=True, max_length=1, null=True)),
                ('latetoday', models.BooleanField(default=False)),
                ('absenttoday', models.BooleanField(default=True)),
            ],
        ),
    ]
