from django.forms import ModelForm, FileInput, Select
from .models import Document

class DocForm(ModelForm):
	class Meta:
		model = Document
		exclude = ['is_published', 'uploaded_by' ]
		widgets = {
			'processor': Select(attrs={
				'class': 'form-control', 
				'data-validation': 'required',
				'data-validation-error-msg-required': 'No processor selected'
				}),
			'upload': FileInput(attrs={
				#'style': 'display: none;',
				'data-validation': 'required',
				'data-validation-error-msg-required': 'No file selected'
				}),
			}