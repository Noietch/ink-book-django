from django.shortcuts import render

from rest_framework.viewsets import *

from .models import *
from .serializers import *

# Create your views here.


class ProjectModelViewSet(ModelViewSet):
    serializer_class = ProjectModelSerializer
    queryset = Project.objects.all()

