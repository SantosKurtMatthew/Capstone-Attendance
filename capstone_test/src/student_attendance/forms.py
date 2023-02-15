from django import forms

from .models import AttendanceSubmit, Students, DailyInteger, StartingTime


#ISSUE: Form doesnt change even if page does
#FIND A WAY TO MAKE THE FORM REFRESH AS WELL

class AttendanceForm(forms.ModelForm):
	email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':"Email"}))
	password = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':"Password"}))
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
	class Meta:
		model = StartingTime
		fields = [
			'grade',
			'starttime',
		]

class DeleteStudent(forms.Form):
	studentid = forms.IntegerField()


	
