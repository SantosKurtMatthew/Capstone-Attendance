# Generated by Django 4.1.5 on 2023-03-11 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_attendance', '0018_alter_students_absents'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sections',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.CharField(max_length=20)),
            ],
        ),
    ]