from django.conf import settings
from django.db import models

# Create your models here.

class UserBook(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, blank=True, null=True, verbose_name='Название')
    author = models.CharField(max_length=120, blank=True, null=True, verbose_name='Автор')
    cover = models.URLField(verbose_name='Обложка')