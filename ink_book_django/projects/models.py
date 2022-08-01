from django.db import models

# Create your models here.


class Project(models.Model):
    name = models.CharField(max_length=255)
    team_id = models.IntegerField()

    class Meta:
        verbose_name = "项目"
        verbose_name_plural = verbose_name


class Prototype(models.Model):
    name = models.CharField(max_length=255)
    route = models.CharField(max_length=255)
    project_id = models.IntegerField()

    class Meta:
        verbose_name = "设计原型"
        verbose_name_plural = verbose_name


class UML(models.Model):
    name = models.CharField(max_length=255)
    route = models.CharField(max_length=255)
    project_id = models.IntegerField()

    class Meta:
        verbose_name = "UML图"
        verbose_name_plural = verbose_name


class Document(models.Model):
    name = models.CharField(max_length=255)
    route = models.CharField(max_length=255)
    project_id = models.IntegerField()

    class Meta:
        verbose_name = "文档"
        verbose_name_plural = verbose_name
