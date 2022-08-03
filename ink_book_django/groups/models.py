from django.db import models


class Groups(models.Model):
    name = models.CharField(max_length=10)
    creator = models.IntegerField()
    avatar = models.TextField(default='https://dn-st.teambition.net/teambition/images/logo1.a6464e9c.jpg')


class GroupsRelations(models.Model):
    group_id = models.IntegerField()
    user_id = models.IntegerField()
    status = models.CharField(max_length=10)
