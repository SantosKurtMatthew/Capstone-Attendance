# Generated by Django 4.1.4 on 2023-01-10 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_attendance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='attendance',
            name='password',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='attendance',
            name='submit_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]