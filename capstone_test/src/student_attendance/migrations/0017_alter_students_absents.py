# Generated by Django 4.1.5 on 2023-03-10 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_attendance', '0016_alter_students_absents'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='absents',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=4),
        ),
    ]