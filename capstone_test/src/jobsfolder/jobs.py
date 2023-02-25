from django.conf import settings
from django.db.models import F

from student_attendance.models import DailyInteger, Students, AttendanceSubmit
import random


def schedule_api():
	global randomint
	randomint = random.randint(1000,9999)
	print("randomint is ", randomint)

	#dailyint = DailyInteger(integer=randomint)
	#dailyint.save()
	#Students.objects.all().update(absents = F('absents')+1)
	#Students.objects.all().update(absenttoday=True)
	#Students.objects.all().update(latetoday=False)
	#AttendanceSubmit.objects.all().delete()
	#UNCOMMENT WHEN FINALIZED

	print('the function works!')
	

schedule_api()

