from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout 
from django.contrib.auth.decorators import login_required

from .forms import AttendanceForm, StudentsInfoForm, ChangeStartingTime, DeleteStudent, CustomUserCreationForm, CustomAuthenticationForm
from .models import AttendanceSubmit, Students, DailyInteger, StartingTime

import schedule, time, random
from datetime import datetime



# Create your views here.


def attendancesubmit_view(request):
	form = AttendanceForm(request.POST or None)
	latestobject = DailyInteger.objects.latest('id')
	dailycode = latestobject.integer

	datetimenow = datetime.now()
	timenow = datetimenow.time()
	

	if form.is_valid():
		submittedemail = form.cleaned_data['email']
		currentstudent = Students.objects.get(email=submittedemail)
		currentgradelevel = currentstudent.grade
		gradelevelstarttime = StartingTime.objects.get(grade=currentgradelevel).starttime
		print(currentgradelevel, 'starts at ', gradelevelstarttime)
		form.save()

		if timenow > gradelevelstarttime:
			currentstudent.lates = currentstudent.lates+1
			currentstudent.spr = currentstudent.lates/5
			
			currentstudent.latetoday = True
			

		currentstudent.absenttoday = False
		currentstudent.absents = currentstudent.absents-1 
		currentstudent.save()
		#Students.objects.all().update(absents = F('absents')*0)#Just to reset the absents
		return HttpResponseRedirect(reverse("attendance_submit"))

	latestobject = DailyInteger.objects.latest('id')#this is to get the latest entry in the field
	
	context = {
		'form':form,
		'latestobject':latestobject,#context for latest entry in the field
		'timenow':timenow,
		#'gradelevelstarttime':gradelevelstarttime,
		
	}
	return render(request, "attendancesubmit.html", context)

@login_required(login_url='/login/')
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

	
	startingtimes = StartingTime.objects.order_by('grade')
	context = {
		'dailycode':dailycode,
		'form':timeform,
		'startingtimes':startingtimes
	}
	return render(request, "dailycodeandstarttimes.html", context)


def studentdatabase_view(request):
	queryset = Students.objects.all()	

	context = {
		'object_list':queryset,
		
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
		'form':form
	}
	return render(request, 'deletestudent.html', context)



def attendancetoday_view(request):
	allstudents = Students.objects.all()
	datetoday = datetime.today().strftime('%m-%d-%Y')
	context = {
		'object_list':allstudents,
		'datetoday':datetoday,
	}
	return render(request, 'dailyattendance.html', context)

def navbar_view(request):
	submitpage = reverse('attendance_submit')
	context = {
		'submitpage':submitpage,
	}
	return render(request, 'navbar.html', context)

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
	return render(request, 'accountcreation.html', context)


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
		'form':form
	}
	return render(request, 'accountlogin.html', context)

def logout_view(request):
	if request.method == "POST":
		logout(request)
		return HttpResponseRedirect(reverse("attendance_submit"))

def instructions_view(request):
	return render(request, 'instructions.html', {})
