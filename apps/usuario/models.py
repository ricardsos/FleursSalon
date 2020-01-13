from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Colaborador(User):
	def __str__(self):
		return self.last_name + ", " + self.first_name

	class Meta:
		verbose_name = 'Colaborador'
		verbose_name_plural = 'Colaboradores'