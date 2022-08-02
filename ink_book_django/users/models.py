from django.db import models
from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):
    cur_group = models.IntegerField(default=0)
    avatar = models.TextField(null=True)
    user_name = models.CharField(max_length=20, null=True)
    real_name = models.CharField(max_length=10, null=True)
