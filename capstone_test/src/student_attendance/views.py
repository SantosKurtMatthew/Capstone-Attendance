from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import F

from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required

from .forms import (
	AttendanceForm, 
	StudentsInfoForm, 
	ChangeStartingTime, 
	DeleteStudent, 
	CustomUserCreationForm, 
	CustomAuthenticationForm, 
	CustomPasswordChangeForm
	)

from .models import (
	AttendanceSubmit, 
	Students, 
	DailyInteger, 
	StartingTime)

import time, random
from datetime import datetime



# Create your views here.
def attendancesubmit_view(request):
	form = AttendanceForm(request.POST or None)

	timenow = datetime.now().time()
	
	if form.is_valid():
		submittedemail = form.cleaned_data['email']
		currentstudent = Students.objects.get(email=submittedemail)
		currentgradelevel = currentstudent.grade
		gradelevelstarttime = StartingTime.objects.get(grade=currentgradelevel).starttime
		print(currentgradelevel, 'starts at ', gradelevelstarttime)
		form.save()

		if timenow > gradelevelstarttime:
			currentstudent.lates = currentstudent.lates+1
			currentstudent.latetoday = True
			
		currentstudent.absenttoday = False
		currentstudent.absents = currentstudent.absents-1 
		currentstudent.spr = currentstudent.lates/5
		currentstudent.save()
		#Students.objects.all().update(absents = F('absents')*0)#Just to reset the absents
		return HttpResponseRedirect(reverse("attendance_submit"))
	
	context = {
		'form':form,
	}
	return render(request, "attendancesubmit.html", context)

def instructions_view(request):
	return render(request, 'instructions.html', {})

@login_required(login_url='/login/')
def dailypassword_view(request):
	latestobject = DailyInteger.objects.latest('id')
	dailycode = latestobject.integer
	creationdate = latestobject.creation_time.date()

	datetoday = datetime.now().date()
	pressedtoday = False

	if creationdate < datetoday:
		pressedtoday = False 
	else:
		pressedtoday = True

	context = {
		'dailycode': dailycode,
		'pressedtoday': pressedtoday
	}
	return render(request, "dailypassword.html", context)

@login_required(login_url='/login/')
def startingtimes_view(request):
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
		
		return HttpResponseRedirect(reverse("starttime"))
	startingtimes = StartingTime.objects.order_by('grade')

	context={
		'form':timeform,
		'startingtimes':startingtimes
	}
	return render(request, 'startingtimes.html', context)

def attendancetoday_view(request):
	allstudents = Students.objects.order_by('classnumber')
	datetoday = datetime.today().strftime('%m-%d-%Y')

	context = {
		'object_list':allstudents,
		'datetoday':datetoday,
	}
	return render(request, 'dailyattendance.html', context)

def studentdatabase_view(request):
	allstudents = Students.objects.order_by('classnumber')	
	context = {
		'object_list':allstudents,	
	}
	return render(request, 'studentdatabase.html', context)

@login_required(login_url='/login/')
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

@login_required(login_url='/login/')
def deletestudent_view(request):
	form = DeleteStudent(request.POST or None)
	if form.is_valid():
		submitted_id = form.cleaned_data['studentid']
		student_to_delete = Students.objects.get(id=submitted_id).delete()
		return HttpResponseRedirect(reverse("delete_studentinfo"))

	context = {
		'form':form,
	}
	return render(request, 'deletestudent.html', context)

@login_required(login_url='/login/')
def accountcreate_view(request):
	if request.method == "POST":
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
	else:
		form = CustomUserCreationForm()

	context = {
		'form':form
	}
	return render(request, 'account/create.html', context)

def login_view(request):
	if request.method == "POST":
		form = CustomAuthenticationForm(data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			if 'next' in request.POST:
				return redirect(request.POST.get('next'))
			else:
				return HttpResponseRedirect(reverse("attendance_submit"))
	else:
		form = CustomAuthenticationForm()

	context = {
		'form':form,
	}
	return render(request, 'account/login.html', context)

def logout_view(request):
	if request.method == "POST":
		logout(request)
		return HttpResponseRedirect(reverse("attendance_submit"))

def passwordchange_view(request):
	if request.method == "POST":
		form = CustomPasswordChangeForm(data=request.POST, user=request.user)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			return HttpResponseRedirect(reverse("attendance_submit"))
	else:
		form = CustomPasswordChangeForm(user=request.user)
	context ={
		'form':form
	}
	return render(request, 'account/change-password.html', context)


def dailyfunction_view(request):
	randomint = random.randint(1000,9999)
	dailyint = DailyInteger(integer=randomint)
	dailyint.save()
	Students.objects.all().update(absents = F('absents')+1)
	Students.objects.all().update(absenttoday=True)
	Students.objects.all().update(latetoday=False)
	AttendanceSubmit.objects.all().delete()
	return HttpResponseRedirect(reverse("attendance_code"))

def purgedatabase_view(request):
	AttendanceSubmit.objects.all().delete()
	Students.objects.all().delete()
	DailyInteger.objects.all().delete()
	return HttpResponseRedirect(reverse("delete_studentinfo"))

