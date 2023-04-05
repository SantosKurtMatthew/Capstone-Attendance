from django.db import models

# Create your models here.
class AttendanceSubmit(models.Model):
	email = models.EmailField(blank=True, null=True)
	password = models.IntegerField(default=0000)
	sessionkey = models.CharField(max_length=50, default='')
	submit_time = models.DateTimeField(auto_now=True)

class Students(models.Model):
	lrn = models.IntegerField(primary_key=True, default=0)
	email = models.EmailField(default='')
	grade = models.IntegerField(default=0)
	section = models.CharField(max_length=10, default='')
	classnumber = models.IntegerField(default=0)
	sex = models.CharField(max_length=1, default='M')
	lates = models.IntegerField(default=0)
	absents = models.FloatField(default=0)
	spr = models.IntegerField(default=0)
	latetoday = models.BooleanField(default=False)
	absenttoday = models.BooleanField(default=True)

class DailyInteger(models.Model):
	integer = models.IntegerField(default=0)
	creation_time = models.DateTimeField(auto_now=True)

class StartingTime(models.Model):
	grade = models.IntegerField(default=0)
	starttime = models.TimeField(default='7:00')

class SectionList(models.Model):
	section = models.CharField(max_length=20)
	highschool = models.CharField(max_length=3, default='shs')



