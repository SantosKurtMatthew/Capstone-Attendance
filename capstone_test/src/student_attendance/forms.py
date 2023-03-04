from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User

from .models import AttendanceSubmit, Students, DailyInteger, StartingTime


#ISSUE: Form doesnt change even if page does
#FIND A WAY TO MAKE THE FORM REFRESH AS WELL

class AttendanceForm(forms.ModelForm):
	email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':"Email"}), label='')
	password = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':" Daily Password"}), label='')
	class Meta:
		model = AttendanceSubmit
		fields = [
			'email',
			'password',
		]

	def clean_email(self, *args, **kwargs):
		cleanemail = self.cleaned_data.get('email')
		existsStudents = Students.objects.filter(email=cleanemail).exists()
		existsAtttendanceSubmit = AttendanceSubmit.objects.filter(email=cleanemail).exists()
		
		print('did he submit today?', existsAtttendanceSubmit)
		if existsStudents == False:
			raise forms.ValidationError('student does not exist')
		if existsAtttendanceSubmit == True:
			raise forms.ValidationError('you submitted today already')
		else:
			return cleanemail

	def clean_password(self, *args, **kwargs):
		dailycode = DailyInteger.objects.latest('id').integer
		cleanpassword = self.cleaned_data.get('password')
		
		if cleanpassword == dailycode:
			return cleanpassword
		else: 
			raise forms.ValidationError('wrong code')
	

class StudentsInfoForm(forms.ModelForm):
	email = forms.EmailField(widget=forms.TextInput(attrs={
		'placeholder':"Email",
		}), label='')
	grade = forms.IntegerField(widget=forms.TextInput(attrs={
		'placeholder':"Grade Level",
		'required':True,
		}), label='')
	section = forms.CharField(widget=forms.TextInput(attrs={
		'placeholder':"Section",
		}), label='')
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
	class Meta:
		model = Students
		fields = [
			'email',
			'grade',
			'section',
			'classnumber',
			'sex',
		]

	def clean_email(self, *args, **kwargs):
		cleanemail = self.cleaned_data.get('email')
		existsStudents = Students.objects.filter(email=cleanemail).exists()
		
		if existsStudents == True:
			raise forms.ValidationError('student already exists')
		else: 
			return cleanemail

class ChangeStartingTime(forms.ModelForm):
	grade = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':"Grade Level"}), label='')
	starttime = forms.TimeField(widget=forms.TextInput(attrs={'placeholder':"Start Time"}), label='')
	class Meta:

		model = StartingTime
		fields = [
			'grade',
			'starttime',
		]

class DeleteStudent(forms.Form):
	studentid = forms.IntegerField(widget=forms.TextInput(attrs={
		'placeholder':"Student's Database ID",
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