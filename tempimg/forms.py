from django import forms

from tempimg.models import TempImg

class TempImgForm(forms.ModelForm):

	class Meta:
		model = TempImg
		fields = ('img',)