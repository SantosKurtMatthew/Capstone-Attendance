from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import F

from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from .forms import (
	AttendanceForm, 
	StudentsInfoForm, 
	ChangeStartingTime, 
	DeleteStudent, 
	CustomUserCreationForm, 
	CustomAuthenticationForm, 
	CustomPasswordChangeForm,
	AddSection,
	PdfFilterForm
	)

from .models import (
	AttendanceSubmit, 
	Students, 
	DailyInteger, 
	StartingTime,
	SectionList
	)

import time, random
from datetime import datetime
from functools import partial


# Create your views here.
def attendancesubmit_view(request):
	form = AttendanceForm(request.POST or None)

	timenow = datetime.now().time()
	
	if form.is_valid():
		submittedemail = form.cleaned_data['email']
		currentstudent = Students.objects.get(email=submittedemail)
		currentgradelevel = currentstudent.grade
		gradelevelstarttime = StartingTime.objects.get(grade=currentgradelevel).starttime
		form.save()

		ishalfday = form.cleaned_data['halfday']
		if ishalfday == True:
			currentstudent.absents = currentstudent.absents+0.5
		
		if ishalfday == False:
			currentstudent.absents = currentstudent.absents-1
			if timenow > gradelevelstarttime:
				currentstudent.lates = currentstudent.lates+1
				currentstudent.latetoday = True

		currentstudent.absenttoday = False 
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
	sectionform = AddSection(request.POST or None)

	if 'timesubmit' in request.POST:
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
	elif 'sectionsubmit' in request.POST:
		if sectionform.is_valid():
			sectionform.save()
			return HttpResponseRedirect(reverse("starttime"))
	elif 'sectiondelete' in request.POST:
		if sectionform.is_valid():
			submittedsection = sectionform.cleaned_data['section']
			currentsection = SectionList.objects.get(section=submittedsection)
			currentsection.delete()
			return HttpResponseRedirect(reverse("starttime"))	

	startingtimes = StartingTime.objects.order_by('grade')
	sections = SectionList.objects.order_by('highschool')
	context={
		'timeform':timeform,
		'startingtimes':startingtimes,
		'sectionform':sectionform,
		'sections':sections,
	}
	return render(request, 'startingtimes.html', context)

def dailyattendance_view(request):
	allstudents = Students.objects.order_by('classnumber')
	datetoday = datetime.today().strftime('%m-%d-%Y')
	sections = SectionList.objects.order_by('highschool')
	context = {
		'object_list':allstudents,
		'datetoday':datetoday,
		'sections':sections,
	}
	return render(request, 'dailyattendance.html', context)

def studentdatabase_view(request):
	form = PdfFilterForm(request.POST or None)
	allstudents = Students.objects.order_by('classnumber')
	sections = SectionList.objects.order_by('highschool')
	if request.method == "POST":
		global grade
		grade = request.POST.get('gradeselect')
		global section
		section = request.POST.get('section')
		return exportpdf_view(request)

		
	context = {
		'object_list':allstudents,	
		'sections':sections,
	}
		
	return render(request, 'studentdatabase.html', context)

@login_required(login_url='/login/')
def newstudent_view(request):
	submitbutton = request.POST.get('submit')
	sectionchoices = SectionList.objects.order_by('highschool').values_list('section', 'section')	
	form = StudentsInfoForm(request.POST or None)
	form.fields['section'].choices = sectionchoices  
	

	if form.is_valid():
		submittedemail = form.cleaned_data['email']
		studentexists = Students.objects.filter(email=submittedemail)

		print('does the student exist?', studentexists)
		if studentexists.exists() == True:
			currentstudent = Students.objects.get(email=submittedemail)
			currentstudent.grade = form.cleaned_data['grade']
			currentstudent.section = form.cleaned_data['section']
			currentstudent.classnumber = form.cleaned_data['classnumber']
			currentstudent.save()
			print(form.cleaned_data['grade'], form.cleaned_data['section'], form.cleaned_data['classnumber'])
		else:
			form.save()
		return HttpResponseRedirect(reverse("new_studentinfo"))
	
	print(sectionchoices)
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

def exportpdf_view(request):
	buffer = io.BytesIO()
	pdf = SimpleDocTemplate(buffer,pagesize=A4)
	#Table Start
	queryset = Students.objects.filter(grade=grade, section=section).order_by('classnumber').values_list('classnumber','email','lates','absents','spr')
	colorlist = [colors.Color(245/255,253/255,250/255),colors.Color(179/255,232/255,205/255)]
	querylist = []
	tableheader = ['CN','Email','Lates','Absents','SPRs']
	querylist.append(tableheader)
	for i in queryset:
		querylist.append(list(i))
	table=Table(querylist)
	tablestyles = TableStyle([
		('ALIGN',(0,0),(-1,-1),'CENTER'),
		('ROWBACKGROUNDS',(0,0),(-1,-1), colorlist),
		('TEXTCOLOR',(0,0),(-1,0),colors.white),
		('GRID',(0,0),(-1,-1),1,colors.white),
		('BOX',(0,0),(-1,-1),5,colors.Color(1/255,102/255,52/255)),
		#Header Format Start
		('BACKGROUND',(0,0),(-1,0),colors.Color(1/255,102/255,52/255)),#
		('FONT',(0,0),(-1,0),'Helvetica-Bold',10,12),
		#Header Format End
		])
	table.setStyle(tablestyles)
	#Table End

	headerstyles = ParagraphStyle('header_styles',
		fontName='Helvetica-Bold',
		fontSize=20,
		alignment=1
		)
	
	subheaderstyles = ParagraphStyle('subheader_styles',
		fontName='Helvetica-Bold',
		fontSize=15,
		alignment=1
		)

	header = Paragraph(grade+section+" Attendance", headerstyles)
	datetoday = Paragraph("As of "+str(datetime.now().date()), headerstyles)

	elems = []
	elems.append(header)
	elems.append(Spacer(10,10))
	elems.append(datetoday)
	elems.append(Spacer(10,20))

	elems.append(table)
	
	pdf.build(elems)
	buffer.seek(0)
	
	return FileResponse(buffer, as_attachment=True, filename='database.pdf')
