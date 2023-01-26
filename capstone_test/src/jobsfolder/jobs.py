from django.conf import settings

from student_attendance.models import DailyInteger
import random

intlist = []
def schedule_api():

	global randomint
	randomint = random.randint(1000,9999)
	print("randomint is ",randomint)
	#dailyint = DailyInteger(integer=randomint)
	#dailyint.save()

	
	

schedule_api()

