from django.db import models
from random import randint


class Groups(models.Model):
    AVATARS = [
        'https://dn-st.teambition.net/teambition/images/logo1.a6464e9c.jpg',
        'https://dn-st.teambition.net/teambition/images/logo3.c69aba1a.jpg',
        'https://dn-st.teambition.net/teambition/images/logo5.a07a0ef0.jpg',
        'https://img.alicdn.com/imgextra/i3/O1CN01fYx7ZL1F2WfrXat17_!!6000000000429-2-tps-600-264.png'
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.avatar is None:
            self.avatar = self.AVATARS[randint(0, 3)]

    name = models.CharField(max_length=50)
    creator = models.IntegerField()
    avatar = models.TextField(null=True)


class GroupsRelations(models.Model):
    group_id = models.IntegerField()
    user_id = models.IntegerField()
    status = models.CharField(max_length=10)
    