from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView

from .models import *
from .serializers import *


# Create your views here.
class ProjectListAPIView(APIView):
    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectModelSerializer(instance=projects, many=True)
        res = {
            'code': 1001,
            'msg': '查询成功',
            'data': serializer.data
        }
        return JsonResponse(res)

    def post(self, request):
        serializer = ProjectModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        res = {
            'code': 1001,
            'msg': '添加成功',
            'data': serializer.validated_data
        }
        return JsonResponse(res)


class ProjectDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            project = Project.objects.get(id=pk)
        except Project.DoesNotExist:
            return JsonResponse({
                'code': 1002,
                'msg': '对象不存在',
                'data': None
                })

        serializer = ProjectModelSerializer(instance=project)
        res = {
            'code': 1001,
            'msg': '查询成功',
            'data': serializer.data
        }
        return JsonResponse(res)

    def put(self, request, pk):
        try:
            project = Project.objects.get(id=pk)
        except Project.DoesNotExist:
            return JsonResponse({
                'code': 1002,
                'msg': '对象不存在',
                'data': None
            })

        serializer = ProjectModelSerializer(instance=project, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        res = {
            'code': 1001,
            'msg': '修改成功',
            'data': serializer.validated_data
        }
        return JsonResponse(res)

    def delete(self, request, pk):
        try:
            project = Project.objects.get(id=pk)
        except Project.DoesNotExist:
            return JsonResponse({
                'code': 1002,
                'msg': '对象不存在',
                'data': None
            })

        project.delete()
        res = {
            'code': 1001,
            'msg': '删除成功',
            'data': None
        }
        return JsonResponse(res)
