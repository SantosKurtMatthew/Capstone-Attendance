from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db.models import F
from django.contrib import messages

from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.models import User
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
	AttendanceRecord,
	AttendanceForm, 
	StudentsInfoForm, 
	ChangeStartingTime, 
	DeleteStudent, 
	CustomUserCreationForm, 
	CustomAuthenticationForm, 
	CustomPasswordChangeForm,
	AddSection,
	PdfFilterForm,
	ExcelForm
	)

from .models import (
	AttendanceSubmit, 
	Students, 
	DailyInteger, 
	StartingTime,
	SectionList,
	AbsentList,
	LateList
	)

import time, random
from datetime import datetime, timedelta
from functools import partial

import tablib
from tablib import Dataset
from .resources import StudentResource

searchedstudent = ''
def ip_view(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return HttpResponse("Welcome Home<br>You are visiting from: {}".format(ip))
# Create your views here.
def attendancesubmit_view(request):
	
	form = AttendanceForm(request.POST or None)
	timenow = datetime.now().time()
	successmessage  = True
	
	if not request.session.exists(request.session.session_key):
		request.session.create()
	currentsession = request.session.session_key

	if form.is_valid():
		submittedemail = form.cleaned_data['email']
		currentstudent = Students.objects.get(email=submittedemail)
		currentgradelevel = currentstudent.grade
		gradelevelstarttime = StartingTime.objects.get(grade=currentgradelevel).starttime

		#Three validation conditions
		sessionfilter = AttendanceSubmit.objects.filter(sessionkey=currentsession).exists()
		attendanceSubmitExists = AttendanceSubmit.objects.filter(email=submittedemail).exists()
		ishalfday = form.cleaned_data['halfday']

		if ishalfday == False:
			if sessionfilter == False:#basic submit
				if attendanceSubmitExists == False:
					currentstudent.absents = currentstudent.absents-1
					currentstudent.absenttoday = False 
					if timenow > gradelevelstarttime:
						currentstudent.lates = currentstudent.lates+1
						currentstudent.latetoday = True
					
					form.save()
					attendancesubmitstudent = AttendanceSubmit.objects.get(email=submittedemail)
					attendancesubmitstudent.sessionkey = currentsession
					attendancesubmitstudent.save()
					currentstudent.attendancesubmit = attendancesubmitstudent
					messages.success(request, 'Attendance Submitted!')
					
				else:
					messages.success(request, 'You already submitted!!', extra_tags='repeat')
			else:
				messages.success(request, 'One Attendance per Device!', extra_tags='repeat')

		else:
			if attendanceSubmitExists == True:
				currentstudent.absents = currentstudent.absents+0.5
				messages.success(request, 'Halfday Successful')
			else:
				#currentstudent.absents = currentstudent.absents-0.5
				messages.success(request, "Can't submit halfday without submitting beforehand")
	
		currentstudent.spr = currentstudent.lates/3
		currentstudent.save()
		return HttpResponseRedirect(reverse("attendance_submit"))
	
	context = {
		'form':form,
		'successmessage':successmessage,
	}
	return render(request, "attendancesubmit.html", context)

def instructions_view(request):
	return render(request, 'instructions.html', {})

@login_required(login_url='/login/')
def dailyreset_view(request):
	latestobjectexists = DailyInteger.objects.filter().exists()
	if latestobjectexists == False:
		dailyint = DailyInteger(integer=999)
		dailyint.save()

	latestobject = DailyInteger.objects.latest('id')
	dailycode = latestobject.integer
	newtime = latestobject.creation_time+timedelta(hours=8)
	
	fixeddate = newtime.date()
	datetoday = datetime.now().date()
	pressedtoday = False

	if fixeddate < datetoday:
		pressedtoday = False
	elif dailycode == 999: 
		pressedtoday = False
	else:
		pressedtoday = True
	

	context = {
		'dailycode': dailycode,
		'pressedtoday': pressedtoday
	}
	return render(request, "dailyreset.html", context)

@login_required(login_url='/login/')
def startingtimes_view(request):
	timeform = ChangeStartingTime(request.POST or None)
	sectionform = AddSection(request.POST or None)

	if 'timesubmit' in request.POST:
		if timeform.is_valid():
			submittedgradelevel = timeform.cleaned_data['grade']
			submittedtime = timeform.cleaned_data['starttime']
			submittedlastday = timeform.cleaned_data['lastday']
			checkrecord = StartingTime.objects.filter(grade=submittedgradelevel).exists()

			if checkrecord == True:
				existinggradelevel = StartingTime.objects.get(grade=submittedgradelevel)
				existinggradelevel.starttime = submittedtime
				existinggradelevel.lastday = submittedlastday
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
	attendancerecordform = AttendanceRecord(request.POST or None)
	sectionchoices = SectionList.objects.order_by('highschool').values_list('section', 'section')
	attendancerecordform.fields['section'].choices = sectionchoices
	datetoday = datetime.today().strftime('%m-%d-%Y')
	global dailyattendanceresults
	dailyattendanceresults = Students.objects.all()
	if request.method == 'POST':
		if 'dailyattendance' in request.POST:
			#global searchedgrade
			searchedgrade = request.POST.get('grade')
			#global searchedsection
			searchedsection = request.POST.get('section')
			submitted = request.POST.get('submitted')
			notsubmitted = request.POST.get('notsubmitted')
		
			print(searchedgrade,searchedsection)
			print(submitted, notsubmitted)
			
			
			if notsubmitted == 'on' and submitted == None:
				dailyattendanceresults = Students.objects.filter(grade=searchedgrade, section=searchedsection, attendancesubmit=None)	
			elif submitted == 'on' and notsubmitted == None:
				dailyattendanceresults = Students.objects.filter(grade=searchedgrade, section=searchedsection).exclude(attendancesubmit=None)
			else: 
				dailyattendanceresults = Students.objects.filter(grade=searchedgrade, section=searchedsection)
	
		elif 'exportpdfdaily' in request.POST:
			return exportpdfdailyattendance_view(request)

	context = {
		'object_list':dailyattendanceresults,
		'datetoday':datetoday,
		'attendancerecord':attendancerecordform,
	}
	return render(request, 'dailyattendance.html', context)

def totalattendance_view(request):
	#form = PdfFilterForm(request.POST or None)
	#allstudents = Students.objects.order_by('classnumber')
	#sections = SectionList.objects.order_by('highschool')
	#if request.method == "POST":
		#global grade
		#grade = request.POST.get('gradeselect')
		#global section
		#section = request.POST.get('section')
		#return exportpdftotalattendance_view(request)
#
	#context = {
		#'object_list':allstudents,
		#'sections':sections,
	#}

	attendancerecordform = AttendanceRecord(request.POST or None)
	sectionchoices = SectionList.objects.order_by('highschool').values_list('section', 'section')
	attendancerecordform.fields['section'].choices = sectionchoices
	datetoday = datetime.today().strftime('%m-%d-%Y')
	global totalattendanceresults
	totalattendanceresults = Students.objects.all()
	if request.method == 'POST':
		if 'totalattendance' in request.POST:
			#global searchedgrade
			searchedgrade = request.POST.get('grade')
			#global searchedsection
			searchedsection = request.POST.get('section')
			submitted = request.POST.get('submitted')
			notsubmitted = request.POST.get('notsubmitted')
		
			print(searchedgrade,searchedsection)
			print(submitted, notsubmitted)
			
			
			if notsubmitted == 'on' and submitted == None:
				totalattendanceresults = Students.objects.filter(grade=searchedgrade, section=searchedsection, attendancesubmit=None)	
			elif submitted == 'on' and notsubmitted == None:
				totalattendanceresults = Students.objects.filter(grade=searchedgrade, section=searchedsection).exclude(attendancesubmit=None)
			else: 
				totalattendanceresults = Students.objects.filter(grade=searchedgrade, section=searchedsection)
	
		elif 'exportpdftotal' in request.POST:
			return exportpdftotalattendance_view(request)

	context = {
		'object_list':totalattendanceresults,
		'datetoday':datetoday,
		'attendancerecord':attendancerecordform,
	}	
	return render(request, 'totalattendance.html', context)

@login_required(login_url='/login/')
def newstudentform_view(request):
	submitbutton = request.POST.get('submit')
	sectionchoices = SectionList.objects.order_by('highschool').values_list('section', 'section')	
	form = StudentsInfoForm(request.POST or None)
	form.fields['section'].choices = sectionchoices
	
	if form.is_valid():
		form.save()
		submittedemail = form.cleaned_data['email']
		currentstudent = Students.objects.get(email=submittedemail)
		currentstudent.spr = currentstudent.lates/3
		currentstudent.save()
		messages.success(request, 'Student Inserted!')
		return HttpResponseRedirect(reverse("new_studentform"))

	context = {
		'form':form,
	}
	return render(request, 'newstudentviaform.html', context)

@login_required(login_url='/login/')
def newstudentexcel_view(request):
	submitbutton = request.POST.get('submit')
	excelform = ExcelForm(request.POST, request.FILES)
	
	if request.method == "POST":
		if excelform.is_valid():
			student_resource = StudentResource()
			excelfile = request.FILES['student_excel']
			filedata = tablib.Dataset().load(excelfile.read(), format='xlsx')
			for data in filedata:
				if str(data[0]).isdigit():
					sprcount = int(data[6])/3
				else:
					sprcount = 0
				value = Students(
						data[0],
						data[1],
						data[2],
						data[3],
						data[4],
						data[5],
						data[6],
						data[7],
						data[8],
						data[9],
						sprcount,
					)
				if str(data[0]).isdigit():
					value.save()
				else:
					pass

			messages.success(request, 'Students Inserted!')
		return HttpResponseRedirect(reverse("new_studentexcel"))

	context = {
		'excelform':excelform
	}
	
	return render(request, 'newstudentviaexcel.html', context)

@login_required(login_url='/login/')
def deletestudent_view(request):
	form = DeleteStudent(request.POST or None)
	if form.is_valid():
		email = form.cleaned_data['email']
		student_to_delete = Students.objects.get(email=email)
		student_to_delete.delete()
		submitted_email = student_to_delete.email
		submission = {'submitted_email':submitted_email}
		
		messages.success(request, f'{submitted_email} Deleted!')
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
			messages.success(request, 'Account Created!')
			return HttpResponseRedirect(reverse("attendance_submit"))
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
			messages.success(request, 'Password Changed!')
			return HttpResponseRedirect(reverse("attendance_submit"))
	else:
		form = CustomPasswordChangeForm(user=request.user)
	context ={
		'form':form
	}
	return render(request, 'account/change-password.html', context)

def absenthistory_view(request):
	if 'search' in request.POST:
		global searchedstudent
		searchedstudent = request.POST.get('searchedstudent')
		results = AbsentList.objects.filter(student__email__contains=searchedstudent)

		context = {
			'searchedstudent':searchedstudent,
			'results':results
			}
		return render(request, 'absenthistory.html', context)
	elif 'exportpdfabsents' in request.POST:
		return exportpdfhistory_view(request)

		
	return render(request, 'absenthistory.html', {})

def latehistory_view(request):
	if 'search' in request.POST:
		global searchedstudent
		searchedstudent = request.POST.get('searchedstudent')
		results = LateList.objects.filter(student__email__contains=searchedstudent)

		context = {
			'searchedstudent':searchedstudent,
			'results':results
			}
		return render(request, 'latehistory.html', context)
	elif 'exportpdflates' in request.POST:
		return exportpdfhistory_view(request)
	return render(request, 'latehistory.html', {})

def dailyfunction_view(request):
	dailypassword = DailyInteger.objects.latest('id')

	if not (dailypassword.integer == 999):
		absentees = Students.objects.filter(absenttoday=True)
		lates = Students.objects.filter(latetoday=True)
		attendancesubmitexists = AttendanceSubmit.objects.filter().exists()
		if attendancesubmitexists == True:
			yesterday = AttendanceSubmit.objects.latest('id').submit_time
			dateyesterday = yesterday.date()+timedelta(1)
			for i in absentees:
				a = AbsentList(student=i, absentdate=dateyesterday)
				a.save()
			for i in lates:
				print(i.email)
				attsub = AttendanceSubmit.objects.get(email=i.email)
				fixedtime = attsub.submit_time+timedelta(hours=8)
				submittime = fixedtime.time()
				b = LateList(student=i, submittime=submittime, latedate=dateyesterday)
				b.save()
		else:
			pass
	else:
		pass

	#Generating the Daily Password
	randomint = random.randint(1000,9999)
	dailyint = DailyInteger(integer=randomint)
	dailyint.save()

	#Resetting the Students' Attendance
	for i in StartingTime.objects.all().order_by('grade'):
		gradelevel = i.grade
		lastday = i.lastday
		today = datetime.today().date()
		if today <= lastday:
			Students.objects.filter(grade=gradelevel).update(absents = F('absents')+1)
			Students.objects.filter(grade=gradelevel).update(absenttoday=True)
			Students.objects.filter(grade=gradelevel).update(latetoday=False)
			AttendanceSubmit.objects.all().delete()
		else: 
			pass
	
	return HttpResponseRedirect(reverse("attendance_code"))

def purgedatabase_view(request):
	AttendanceSubmit.objects.all().delete()
	Students.objects.all().delete()
	DailyInteger.objects.all().delete()
	StartingTime.objects.all().delete()
	SectionList.objects.all().delete()
	User.objects.filter(is_superuser=False).delete()
	return HttpResponseRedirect(reverse("delete_studentinfo"))

def exportpdftotalattendance_view(request):
	buffer = io.BytesIO()
	pdf = SimpleDocTemplate(buffer,pagesize=A4)
	
	#Table Start
	colorlist = [colors.Color(245/255,253/255,250/255),colors.Color(179/255,232/255,205/255)]
	querylist = []
	tableheader = ['CN','Email','Lates','Absents','SPRs']
	querylist.append(tableheader)
	queryset = totalattendanceresults.values_list('classnumber','email','lates','absents','spr')

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

	pdfname = str(totalattendanceresults[0].grade)+totalattendanceresults[0].section
	header = Paragraph(pdfname+" Attendance", headerstyles)
	datetoday = Paragraph("As of "+str(datetime.now().date()), headerstyles)

	elems = []
	elems.append(header)
	elems.append(Spacer(10,10))
	elems.append(datetoday)
	elems.append(Spacer(10,20))
	elems.append(table)
	
	pdf.build(elems)
	buffer.seek(0)
	
	return FileResponse(buffer, as_attachment=True, filename=pdfname+"_totalattendance.pdf")

def exportpdfdailyattendance_view(request):
	buffer = io.BytesIO()
	pdf = SimpleDocTemplate(buffer,pagesize=A4)
	#Table Start
	colorlist = [colors.Color(245/255,253/255,250/255),colors.Color(179/255,232/255,205/255)]
	querylist = []
	tableheader = ['CN','Email','Late','Absent','Time']
	querylist.append(tableheader)
	queryset = dailyattendanceresults.values_list('classnumber','email','latetoday','absenttoday','attendancesubmit__submit_time')
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

	pdfname = str(dailyattendanceresults[0].grade)+dailyattendanceresults[0].section
	header = Paragraph(pdfname+" Attendance", headerstyles)
	datetoday = Paragraph("On "+str(datetime.now().date()), headerstyles)

	
	elems = []
	elems.append(header)
	elems.append(Spacer(10,10))
	elems.append(datetoday)
	elems.append(Spacer(10,20))
	elems.append(table)
	
	pdf.build(elems)
	buffer.seek(0)
	
	return FileResponse(buffer, as_attachment=True, filename=pdfname+"_totalattendance.pdf")

def exportpdfhistory_view(request):
	buffer = io.BytesIO()
	pdf = SimpleDocTemplate(buffer,pagesize=A4)
	
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
	
	print(searchedstudent, "the searched student")
	pdfname = searchedstudent
	datetoday = Paragraph("As of "+str(datetime.now().date()), headerstyles)

	if 'exportpdfabsents' in request.POST:
		queryset = AbsentList.objects.filter(student__email__contains=searchedstudent).values_list('student__email','student__grade','student__section','absentdate','student__absents')
		tableheader = ['Email','Grade','Section','Date','Total Absents']
		header = Paragraph(pdfname+" Absents", headerstyles)
		filename = '_absents.pdf'
	elif 'exportpdflates' in request.POST:
		queryset = LateList.objects.filter(student__email__contains=searchedstudent).values_list('student__email','student__grade','student__section','latedate','student__lates','submittime')
		tableheader = ['Email','Grade','Section','Date','Total Lates','Submit Time']
		header = Paragraph(pdfname+" Lates", headerstyles)
		filename = '_lates.pdf'
	
	
	colorlist = [colors.Color(245/255,253/255,250/255),colors.Color(179/255,232/255,205/255)]
	querylist = []
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

	elems = []
	elems.append(header)
	elems.append(Spacer(10,10))
	elems.append(datetoday)
	elems.append(Spacer(10,20))
	if 'exportpdfabsents' in request.POST:
		elems.append(Paragraph("*If a student's total absents do not match with number of dates, they most likely have not submitted their attendance today"))
		elems.append(Spacer(10,10))
	elems.append(table)

	
	pdf.build(elems)
	buffer.seek(0)
	
	return FileResponse(buffer, as_attachment=True, filename=pdfname+filename)

