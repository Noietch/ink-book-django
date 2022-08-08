from rest_framework import serializers
from .models import *


class GroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groups
        fields = "__all__"
        exclude = ('file_system',)


class GroupsRelationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupsRelations
        fields = "__all__"
