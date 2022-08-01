from django.db import models
from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):
    avatar = models.TextField(null=True)
    real_name = models.CharField(max_length=10, null=True)
