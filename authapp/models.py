from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class MyBookUser(AbstractUser):
    sessionCookie = models.CharField(max_length=150, blank=True, null=True)