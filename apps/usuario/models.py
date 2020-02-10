from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Colaborador(User):
	def __str__(self):
		return self.first_name + " " + self.last_name

	class Meta:
		verbose_name = 'Colaborador'
		verbose_name_plural = 'Colaboradores'