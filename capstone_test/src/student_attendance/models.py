from django.db import models

# Create your models here.
class AttendanceSubmit(models.Model):
	email = models.EmailField(blank=True, null=True)
	password = models.IntegerField(default=0000)
	submit_time = models.DateTimeField(auto_now=True)

class Students(models.Model):
	email = models.EmailField(default='')
	grade = models.IntegerField(default=0)
	section = models.CharField(max_length=10, default='')
	classnumber = models.IntegerField(default=0)
	lates = models.IntegerField(default=0)
	absents = models.IntegerField(default=0)
	spr = models.IntegerField(default=0)
	sexchoices=(
		('M',"M"),
		('F',"F")
		)
	sex = models.CharField(max_length=1, blank=True, null=True, choices=sexchoices)
	latetoday = models.BooleanField(default=False)
	absenttoday = models.BooleanField(default=True)

class DailyInteger(models.Model):
	integer = models.IntegerField(default=0)
	creation_time = models.DateTimeField(auto_now=True)

class StartingTime(models.Model):
	grade = models.IntegerField(default=0)
	starttime = models.TimeField(default='7:00')

class TeacherPasswords(models.Model):
	password = models.CharField(max_length=30, default='')
