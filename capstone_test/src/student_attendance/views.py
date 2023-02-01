from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import AttendanceForm, StudentsInfoForm, ChangeStartingTime
from .models import Attendance, Students, DailyInteger, StartingTime

import schedule, time, random
from datetime import datetime



# Create your views here.


#THIS ONE SHOULD BE DELETED WHEN ALL PAGES ARE DONE
def homepage_view(request, *args, **kwargs):
	return render(request, "homepage.html", {})


def attendancesubmit_view(request):
	form = AttendanceForm(request.POST or None)
	latestobject = DailyInteger.objects.latest('id')
	dailycode = latestobject.integer

	datetimenow = datetime.now()
	timenow = datetimenow.time()
	#latetime = timenow.replace(hour=17, minute=0, second=0)

	if form.is_valid():
		submittedemail = form.cleaned_data['email']
		currentstudent = Students.objects.get(email=submittedemail)
		currentgradelevel = currentstudent.grade
		gradelevelstarttime = StartingTime.objects.get(grade=currentgradelevel).starttime
		print(currentgradelevel, 'starts at ', gradelevelstarttime)

		if timenow > gradelevelstarttime:
			currentstudent.lates = currentstudent.lates+1
			currentstudent.save()
			print(submittedemail, 'is late so he gets +1')


		return HttpResponseRedirect(reverse("attendance_submit"))

	latestobject = DailyInteger.objects.latest('id')#this is to get the latest entry in the field
	
	context = {
		'form':form,
		'latestobject':latestobject,#context for latest entry in the field
		'timenow':timenow,
		#'gradelevelstarttime':gradelevelstarttime,
		
	}
	return render(request, "attendancesubmit.html", context)


def attendancecode_view(request):
	latestobject = DailyInteger.objects.latest('id')
	dailycode = latestobject.integer

	timeform = ChangeStartingTime(request.POST or None)

	if timeform.is_valid():
		submittedgradelevel = timeform.cleaned_data['grade']
		submittednewtime = timeform.cleaned_data['starttime']
		checkrecord = StartingTime.objects.filter(grade=submittedgradelevel).exists()

		if checkrecord == True:
			existinggradelevel = StartingTime.objects.get(grade=submittedgradelevel)
			existinggradelevel.starttime = submittednewtime
			existinggradelevel.save()
		else:
			timeform.save()	
		print("Does the record exist? ",checkrecord)

		
		return HttpResponseRedirect(reverse("attendance_code"))

	startingtimes = StartingTime.objects.all()

	context = {
		'dailycode':dailycode,
		'form':timeform,
		'startingtimes':startingtimes
	}
	return render(request, "attendancecode.html", context)


def studentdatabase_view(request):
	queryset = Students.objects.all()	

	context = {
		'object_list':queryset,
		
	}
	return render(request, 'studentdatabase.html', context)


def newstudent_view(request):
	submitbutton = request.POST.get('submit')
	form = StudentsInfoForm(request.POST or None)
	if form.is_valid():
		form.save()
		return HttpResponseRedirect(reverse("new_studentinfo"))

	context = {
		'form':form,
	}
	return render(request, 'newstudent.html', context)

def navbar_view(request):
	submitpage = reverse('attendance_submit')
	context = {
		'submitpage':submitpage,
	}
	return render(request, 'navbar.html', context)


