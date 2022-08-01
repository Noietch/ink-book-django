from django.db import models


class Groups(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)
    creator = models.IntegerField()


class GroupsRelations(models.Model):
    group_id = models.IntegerField()
    user_id = models.IntegerField()
    status = models.CharField(max_length=10)
