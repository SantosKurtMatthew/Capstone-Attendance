from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import AttendanceForm, StudentsInfoForm
from .models import Attendance, Students, DailyInteger

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

	if form.is_valid():
		submittedemail = form.cleaned_data['email']
		currentstudent = Students.objects.get(email=submittedemail)
		currentstudent.lates = currentstudent.lates+1
		currentstudent.save()


		
		print('the email used is ', submittedemail)
		return HttpResponseRedirect(reverse("attendance_submit"))

	latestobject = DailyInteger.objects.latest('id')#this is to get the latest entry in the field
	
	context = {
		'form':form,
		'latestobject':latestobject#context for latest entry in the field
		
	}
	return render(request, "attendancesubmit.html", context)


def attendancecode_view(request):
	latestobject = DailyInteger.objects.latest('id')
	dailycode = latestobject.integer


	context = {
		'dailycode':dailycode
	}
	return render(request, "attendancecode.html", context)


def studentdatabase_view(request):
	queryset = Students.objects.all()
	
	#queryset = Attendance.objects.filter(email='kurtsantos924@gmail.com')

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


