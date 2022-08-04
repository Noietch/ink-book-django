from rest_framework.serializers import ModelSerializer, ValidationError

from .views import *


class ProjectModelSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = "__all__"


class PrototypeModelSerializer(ModelSerializer):

    class Meta:
        model = Prototype
        fields = "__all__"


class UMLModelSerializer(ModelSerializer):

    class Meta:
        model = UML
        fields = "__all__"


class DocumentModelSerializer(ModelSerializer):

    class Meta:
        model = Document
        fields = "__all__"
