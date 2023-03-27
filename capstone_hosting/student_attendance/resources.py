from import_export import resources
from .models import Students

class StudentResource(resources.ModelResource):
	class Meta:
		model = Students
		fields = (
			'id',
			'email',
			'grade',
			'section',
			'classnumber',
			'sex',
		)