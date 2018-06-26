from django.db import models

from versatileimagefield.fields import VersatileImageField
from django.contrib.auth.models import User

class TempImg(models.Model):
	img = VersatileImageField(upload_to = 'img/indetify/temp', verbose_name='img')
	user = user =  models.ForeignKey(
		User,
        verbose_name = 'usuario'		
		)
	created_at = models.DateTimeField(auto_now_add = True)
	

	def __str__(self):
		return self.img.name
