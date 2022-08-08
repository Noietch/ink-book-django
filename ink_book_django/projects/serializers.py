from rest_framework.serializers import *

from .models import Project, Prototype, UML, Document, StarProject


class ProjectModelSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = "__all__"


class StarProjectModelSerializer(ModelSerializer):

    class Meta:
        model = StarProject
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
