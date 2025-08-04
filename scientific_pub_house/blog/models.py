from django.db import models
from core.models import PubCreateModel
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class Magazine(PubCreateModel):
	title = models.CharField(max_length=256, verbose_name='Заголовок')
	description = models.TextField(verbose_name='Описание')
	slug = models.SlugField(
		verbose_name='Идентификатор',
		help_text='Идентификатор страницы для URL; '
				  'разрешены символы латиницы, цифры, дефис и подчёркивание.',
		unique=True,
	)

	class Meta:
		verbose_name = 'журнал'
		verbose_name_plural = 'Журналы'

	def __str__(self):
		return self.title


class Post(PubCreateModel):
	title = models.CharField(max_length=256, verbose_name='Название')
	text = models.TextField(verbose_name='Текст')
	pub_date = models.DateTimeField(
		verbose_name='Дата и время публикации',
		help_text='Если установить дату и время в будущем — '
				  'можно делать отложенные публикации.'
	)
	author = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='posts',
		verbose_name='Автор публикации',
	)
	image = models.ImageField(
		'Фото', upload_to='images', blank=True
	)
	magazine = models.ForeignKey(
		Magazine,
		on_delete=models.SET_NULL,
		null=True,
		blank=False,
		related_name='posts',
		verbose_name='Журнал'
	)

	class Meta:
		verbose_name = 'публикация'
		verbose_name_plural = 'Публикации'

	def get_absolute_url(self):
		return reverse('blog:post_detail', kwargs={'pk': self.pk})

	def __str__(self):
		return self.title


class Comment(PubCreateModel):
	text = models.TextField(verbose_name='Текст комментария')
	post = models.ForeignKey(
		Post,
		on_delete=models.CASCADE,
		related_name='comments',
	)
	created_at = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		ordering = ('created_at',)
