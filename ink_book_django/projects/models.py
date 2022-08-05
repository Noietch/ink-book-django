from django.db import models
from json import loads, dumps


# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=200)
    team_id = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    avatar = models.TextField(default='https://dn-st.teambition.net/teambition/images/logo1.a6464e9c.jpg')
    width = models.IntegerField(default=1440)
    height = models.IntegerField(default=1024)

    class Meta:
        verbose_name = "项目"
        verbose_name_plural = verbose_name


class Prototype(models.Model):
    name = models.CharField(max_length=200)
    route = models.CharField(max_length=255, null=True)
    project_id = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    avatar = models.TextField(default='https://dn-st.teambition.net/teambition/images/logo3.c69aba1a.jpg')
    width = models.IntegerField(default=1440)
    height = models.IntegerField(default=1024)
    components = models.TextField(null=True)

    class Meta:
        verbose_name = "设计原型"
        verbose_name_plural = verbose_name


class UML(models.Model):
    name = models.CharField(max_length=200)
    route = models.CharField(max_length=255, null=True)
    project_id = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    avatar = models.TextField(default='https://dn-st.teambition.net/teambition/images/logo5.a07a0ef0.jpg')
    width = models.IntegerField(default=1440)
    height = models.IntegerField(default=1024)

    class Meta:
        verbose_name = "UML图"
        verbose_name_plural = verbose_name


class Document(models.Model):
    name = models.CharField(max_length=200)
    route = models.CharField(max_length=255, null=True)
    encryption = models.CharField(null=True, max_length=255)
    project_id = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    avatar = models.TextField(default='https://img.alicdn.com/imgextra/i3/O1CN01fYx7ZL1F2WfrXat17_!!6000000000429-2-tps-600-264.png')
    width = models.IntegerField(default=1440)
    height = models.IntegerField(default=1024)

    class Meta:
        verbose_name = "文档"
        verbose_name_plural = verbose_name

#
# class Component(models.Model):
#     acceptRatio = models.BooleanField()
#     active = models.BooleanField()
#     axis = models.CharField(default='xy', max_length=10)
#     children = models.TextField(null=True)
#     draggable = models.BooleanField()
#     extra = models.TextField()
#     grid = models.TextField()
#     id = models.CharField(max_length=50)
#     minHeight = models.IntegerField()
#     minWidth = models.IntegerField()
#     parent = models.BooleanField()
#     parentId = models.IntegerField(null=True)
#     resizable = models.BooleanField()
#     resizeHandler = models.TextField()
#     rotatable = models.BooleanField()
#     transform = models.TextField()
#     type = models.CharField(max_length=50)
#     zoom = models.IntegerField()
