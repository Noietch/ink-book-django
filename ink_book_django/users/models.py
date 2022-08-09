from django.db import models
from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):
    discription = models.TextField(null=True)
    phone = models.CharField(max_length=100, null=True)
    sex = models.CharField(max_length=10, null=True)
    cur_group = models.IntegerField(default=0)
    personal_group = models.IntegerField(default=0)
    avatar = models.TextField(null=True,default="https://www.noietch.cn/resource/logo.png")
    user_name = models.CharField(max_length=100, default='小墨')
    real_name = models.CharField(max_length=100, null=True)
