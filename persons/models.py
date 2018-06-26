from django.db import models
import uuid
from django.contrib.auth.models import User

class Person(models.Model):
	SEX_CHOICES = (
        ('F', 'Femenino',),
        ('M', 'Masculino',),
        ('U', 'Inseguro',),
    )
	id_person = models.CharField( max_length=50, unique=True)
	name = models.CharField(verbose_name='Nombre(s)',max_length=50 )
	last_name = models.CharField(verbose_name='Apellidos',max_length=100)
	date_birth = models.DateField()
	sex = models.CharField(max_length=1, choices=SEX_CHOICES,)
	id_auto = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	user =  models.ForeignKey(
		User,
        verbose_name = 'usuario'		
		)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	personid = models.CharField(max_length=60, unique=True)

	class Meta:
		verbose_name='Sujeto'
		verbose_name_plural = 'Sujetos'

	def __str__(self):
		return self.name