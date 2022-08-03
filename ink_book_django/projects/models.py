from django.db import models


# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=255)
    team_id = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    avatar = models.TextField(default='https://dn-st.teambition.net/teambition/images/logo1.a6464e9c.jpg')

    class Meta:
        verbose_name = "项目"
        verbose_name_plural = verbose_name


class Prototype(models.Model):
    name = models.CharField(max_length=255)
    route = models.CharField(max_length=255)
    project_id = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    avatar = models.TextField(default='https://dn-st.teambition.net/teambition/images/logo3.c69aba1a.jpg')

    class Meta:
        verbose_name = "设计原型"
        verbose_name_plural = verbose_name


class UML(models.Model):
    name = models.CharField(max_length=255)
    route = models.CharField(max_length=255)
    project_id = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    avatar = models.TextField(default='https://dn-st.teambition.net/teambition/images/logo5.a07a0ef0.jpg')

    class Meta:
        verbose_name = "UML图"
        verbose_name_plural = verbose_name


class Document(models.Model):
    name = models.CharField(max_length=255)
    route = models.CharField(max_length=255)
    project_id = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    avatar = models.TextField(default='https://img.alicdn.com/imgextra/i3/O1CN01fYx7ZL1F2WfrXat17_!!6000000000429-2-tps-600-264.png')

    class Meta:
        verbose_name = "文档"
        verbose_name_plural = verbose_name
