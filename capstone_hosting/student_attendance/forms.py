from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User

from .models import AttendanceSubmit, Students, DailyInteger, StartingTime, SectionList
from datetime import datetime, timedelta


class DateInput(forms.DateInput):
	input_type = 'date'

class AttendanceForm(forms.ModelForm):
	email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':"Email",'id':'emailinput'}), label='')
	password = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':" Daily Password"}), label='')
	halfday = forms.BooleanField(widget=forms.CheckboxInput(attrs={'id':'checkbox',}), required=False)
	class Meta:
		model = AttendanceSubmit
		fields = [
			'email',
			'password',
			'halfday'
		]

	def clean_email(self, *args, **kwargs):
		cleanemail = self.cleaned_data.get('email')
		existsStudents = Students.objects.filter(email=cleanemail).exists()
		if existsStudents == False:
			raise forms.ValidationError('student does not exist')
		
		studentgrade = Students.objects.get(email=cleanemail).grade
		existsStartingTime = StartingTime.objects.filter(grade=studentgrade).exists()
		if existsStartingTime == False: #and cleanhalfday == False:
			raise forms.ValidationError('no time set for this grade level')
		else:
			return cleanemail

	def clean_password(self, *args, **kwargs):
		dailycode = DailyInteger.objects.latest('id').integer
		cleanpassword = self.cleaned_data.get('password')
		if cleanpassword == 999:
			raise forms.ValidationError('not a valid code')
		elif cleanpassword == dailycode:
			return cleanpassword
		else: 
			raise forms.ValidationError('wrong code')
	
class ExcelForm(forms.Form):
	student_excel = forms.FileField(widget=forms.FileInput(attrs={
		'id':'fileupload'
		}),required=False, label='')

class StudentsInfoForm(forms.ModelForm):
	lrn = forms.IntegerField(widget=forms.TextInput(attrs={
		'placeholder':"LRN",
		'required':False,
		}), label='')
	email = forms.EmailField(widget=forms.TextInput(attrs={
		'placeholder':"Email",
		}), label='')
	grade = forms.IntegerField(widget=forms.TextInput(attrs={
		'placeholder':"Grade Level",
		'required':True,
		}), label='')
	section = forms.ChoiceField(widget=forms.Select(attrs={
		'required':True,
		'class':'sexselect' 
		}), choices=())
	classnumber = forms.IntegerField(widget=forms.TextInput(attrs={
		'placeholder':"Class Number",
		'required':True,
		}), label='')
	sexchoices=(
		('M',"M"),
		('F',"F")
		)
	sex = forms.ChoiceField(widget=forms.Select(attrs={
		'required':True,
		'class':'sexselect' 
		}),choices=sexchoices)
	lates = forms.IntegerField(widget=forms.TextInput(attrs={
		'placeholder':"Number of Lates",
		}), label='', required=False)
	absents = forms.IntegerField(widget=forms.TextInput(attrs={
		'placeholder':"Number of Absents",
		}), label='', required=False)
	boolchoices=(
		('True', 'Yes'),
		('False',"No")
		)
	latetoday = forms.ChoiceField(widget=forms.Select(attrs={
		'required':False,
		'class':'sexselect' 
		}),choices=boolchoices, label="Late Today", initial=boolchoices[1])
	absenttoday = forms.ChoiceField(widget=forms.Select(attrs={
		'required':False,
		'class':'sexselect' 
		}),choices=boolchoices, label="Absent Today")
	class Meta:
		model = Students
		fields = [
			'lrn',
			'email',
			'grade',
			'section',
			'classnumber',
			'sex',
			'lates',
			'absents',
			'latetoday',
			'absenttoday'
		]

	def clean_lates(self):
		data = self.cleaned_data['lates']
		if not data:
			data = '0'
		return data
	def clean_absents(self):
		data = self.cleaned_data['absents']
		if not data:
			data = '0'
		return data
	


class ChangeStartingTime(forms.ModelForm):
	grade = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':"Grade Level"}), label='')
	starttime = forms.TimeField(widget=forms.TextInput(attrs={'placeholder':"Start Time"}), label='')
	lastday = forms.DateField(widget=DateInput, initial=datetime.today()+timedelta(days=240))
	class Meta:

		model = StartingTime
		fields = [
			'grade',
			'starttime',
			'lastday'
		]

class AddSection(forms.ModelForm):
	section = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Section",'id':'sectioninput'}), label='')
	highschoolchoices = (
		('JHS','JHS'),
		('SHS','SHS')
	)
	highschool = forms.ChoiceField(widget=forms.Select(attrs={
		'required':True,
		'id':'highschoolselect'
		}), choices=highschoolchoices, )
	class Meta:

		model = SectionList
		fields = [
			'section',
			'highschool'
		]

class DeleteStudent(forms.Form):
	email = forms.CharField(widget=forms.TextInput(attrs={
		'placeholder':"Student's email",
		'required':True,
		}), label='')

	def clean_email(self, *args, **kwargs):
		cleanemail = self.cleaned_data.get('email')
		existsStudents = Students.objects.filter(email=cleanemail).exists()

		if existsStudents == False:
			raise forms.ValidationError('student does not exist')
		else:
			return cleanemail

class PdfFilterForm(forms.Form):
	grade = forms.IntegerField(widget=forms.TextInput(attrs={
		'placeholder':"grade level",
		'required':True,
		}), label='')
	section = forms.CharField(widget=forms.TextInput(attrs={
		'placeholder':"section",
		'required':True,
		}), label='')

class CustomUserCreationForm(UserCreationForm):

	class Meta:
		model = User
		fields = [
			'username',
			'password1',
			'password2',	
		]

	def __init__(self, *args, **kwargs):
		super(CustomUserCreationForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['placeholder'] = 'Username'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'

		self.fields['username'].label = ''
		self.fields['password1'].label = ''
		self.fields['password2'].label = ''


class CustomAuthenticationForm(AuthenticationForm):
	class Meta:
		model = User
		fields =[
			'username',
			'password',
		]

	def __init__(self, *args, **kwargs):
		super(CustomAuthenticationForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['placeholder'] = 'Username'
		self.fields['password'].widget.attrs['placeholder'] = 'Password'
		

		self.fields['username'].label = ''
		self.fields['password'].label = ''
		

	
class CustomPasswordChangeForm(PasswordChangeForm):
	class Meta:
		model = User
		fields=[
			'old_password',
			'new_password1',
			'new_password2',
		]

	def __init__(self, *args, **kwargs):
		super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)

		self.fields['old_password'].widget.attrs['placeholder'] = 'Old Password'
		self.fields['new_password1'].widget.attrs['placeholder'] = 'New Password'
		self.fields['new_password2'].widget.attrs['placeholder'] = 'Repeat New Password'
		

		self.fields['old_password'].label = ''
		self.fields['new_password1'].label = ''
		self.fields['new_password2'].label = ''

