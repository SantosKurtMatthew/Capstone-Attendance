# Generated by Django 4.1.5 on 2023-03-11 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_attendance', '0020_rename_sections_sectionlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='sectionlist',
            name='highschool',
            field=models.CharField(default='jhs', max_length=3),
        ),
    ]
