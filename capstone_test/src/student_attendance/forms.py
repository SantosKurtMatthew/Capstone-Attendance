from django import forms

from .models import Attendance, Students, DailyInteger


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

	
	
	def clean_password(self, *args, **kwargs):
		dailycode = DailyInteger.objects.latest('id').integer
		cleanpassword = self.cleaned_data.get('password')
		if cleanpassword == dailycode:
			return cleanpassword
		else: 
			raise forms.ValidationError('wrong code')

	#def checkinteger(self, *args, **kwargs):
		#submittedinteger = self.cleaned_data.get('password')
		#if submittedinteger == dailycode:
			#return submittedinteger
		#else: 
			#raise forms.ValidationError("wrong code")
	

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

	
