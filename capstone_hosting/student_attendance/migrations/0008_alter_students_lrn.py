# Generated by Django 4.1.7 on 2023-04-11 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_attendance', '0007_absentlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='lrn',
            field=models.CharField(default=0, max_length=20, primary_key=True, serialize=False),
        ),
    ]
