from django.db import models

# Create your models here.
class Attendance(models.Model):
	email = models.EmailField(blank=True, null=True)
	password = models.IntegerField(default=0000)
	submit_time = models.DateTimeField(auto_now=True)

class Students(models.Model):
	email = models.EmailField(blank=True, null=True)
	grade = models.IntegerField(default=0)
	section = models.CharField(max_length=10,blank=True, null=True)
	classnumber = models.IntegerField(default=0)
	lates = models.IntegerField(default=0)
	absents = models.IntegerField(default=0)

class DailyInteger(models.Model):
	integer = models.IntegerField(default=0)
	creation_time = models.DateTimeField(auto_now=True)

class StartingTime(models.Model):
	grade = models.IntegerField(default=0)
	starttime = models.TimeField(default='7:00')


