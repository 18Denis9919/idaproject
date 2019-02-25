from django import forms
from .models import Image

class ImageCreateForm(forms.ModelForm):
	class Meta:
		model = Image
		fields = [
			'image_file',
			'image_url'
		]

		labels = {
			'image_file':'File',
			'image_url':'URL'
			}

	def clean(self):
		form_data = self.cleaned_data
		if form_data['image_file'] and form_data['image_url']:
			self._errors["image_url"] = ["Only 1 method"]
		return form_data
