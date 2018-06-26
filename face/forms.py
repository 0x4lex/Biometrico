from django import forms

from face.models import Face

class FaceForm(forms.ModelForm):

	class Meta:
		model = Face
		fields = ('img',)