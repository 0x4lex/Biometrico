from django import forms

from persons.models import Person


SEX_CHOICES = (
    ('F', 'Femenino'),
    ('M', 'Masculino'),
    ('U', 'Inseguro'),
)


class PersonForm(forms.ModelForm):
	sex = forms.ChoiceField(
		choices=SEX_CHOICES,
		widget=forms.Select(attrs={'class': 'form-control input-lg',}),
		)

	class Meta:
		model = Person
		fields = ('id_person','name','last_name','date_birth','sex',)
		widgets = {
			'id_person': forms.TextInput(attrs={'class': 'form-control input-lg','placeholder': 'id'}),
			'name': forms.TextInput(attrs={'class': 'form-control input-lg','placeholder': 'nombre'}),
			'last_name': forms.TextInput(attrs={'class': 'form-control input-lg','placeholder': 'apellidos'}),
			'date_birth': forms.TextInput(attrs={'class': 'form-control input-lg','id': 'datemask'}),
		}