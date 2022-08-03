from rest_framework import serializers
from .models import Users


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id', 'email', 'user_name', 'avatar', 'real_name', 'cur_group')
