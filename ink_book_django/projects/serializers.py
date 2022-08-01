from rest_framework.serializers import ModelSerializer

from .views import Project


class ProjectModelSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = "__all__"
