from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
	email = models.EmailField(
		blank=False,
		max_length=254,
		unique=True,
	)

	class Meta:
		verbose_name = 'Пользователь'
		verbose_name_plural = 'Пользователи'

	def __str__(self):
		return self.username
