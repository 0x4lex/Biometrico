from django.db import models
from persons.models import Person
from django.contrib.auth.models import User

from versatileimagefield.fields import VersatileImageField

class Face(models.Model):
	user =  models.ForeignKey(
		User,
        verbose_name = 'usuario'		
		)
	person =  models.ForeignKey(
		Person,
        verbose_name = 'sujeto'		
		)
	img = VersatileImageField(upload_to = 'img/face', verbose_name='face')
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	faceid = models.CharField(max_length=60, blank=True)

	class Meta:
		verbose_name='Foto'
		verbose_name='Fotos'

	def __str__(self):
		return self.person.name

	def image_url(self):
		return self.img.url