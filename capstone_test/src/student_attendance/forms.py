from django import forms

from .models import Attendance, Students, DailyInteger, StartingTime


#ISSUE: Form doesnt change even if page does
#FIND A WAY TO MAKE THE FORM REFRESH AS WELL

class AttendanceForm(forms.ModelForm):
	email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':"Email"}))
	password = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':"Password"}))
	class Meta:
		model = Attendance
		fields = [
			'email',
			'password',
		]

	def cleanemail(self, *args, **kwargs):
		cleanemail = self.cleaned_data.get('email')
		emailqueryset = Students.objects.filter(email=cleanemail)
		exists = emailqueryset.exists()

		if exists == True:
			return cleanemail
		else:
			raise forms.ValidationError('wrong code')

	def clean_password(self, *args, **kwargs):
		dailycode = DailyInteger.objects.latest('id').integer
		cleanpassword = self.cleaned_data.get('password')
		if cleanpassword == dailycode:
			return cleanpassword
		else: 
			raise forms.ValidationError('wrong code')
	

class StudentsInfoForm(forms.ModelForm):
	class Meta:
		model = Students
		fields = [
			'email',
			'grade',
			'section',
			'classnumber',
			'lates',
			'absents',
		]

class ChangeStartingTime(forms.ModelForm):
	class Meta:
		model = StartingTime
		fields = [
			'grade',
			'starttime',
		]

	
