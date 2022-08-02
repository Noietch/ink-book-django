from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404

from .models import *
from .serializers import *


# Create your views here.
class ListAPIView(APIView):
    model = None
    serializer = None

    def get(self, request):
        objects1 = self.model.objects.filter(is_deleted=False)
        serializer1 = self.serializer(objects1, many=True)
        objects2 = self.model.objects.filter(is_deleted=True)
        serializer2 = self.serializer(objects2, many=True)
        res = {
            'code': 1001,
            'msg': '查询成功',
            'data': [serializer1.data, serializer2.data]
        }
        return Response(res)

    def post(self, request):
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            res = {
                'code': 1001,
                'msg': '添加成功',
                'data': serializer.data
            }
        else:
            res = {
                'code': 1002,
                'msg': '添加失败',
                'data': serializer.data
            }
        return Response(res)


class DetailAPIView(APIView):
    model = None
    serializer = None

    def get_object(self, pk):
        try:
            obj = self.model.objects.get(id=pk)
        except self.model.DoesNotExist:
            raise Http404
        return obj

    def get(self, request, pk):
        obj = self.get_object(pk)

        serializer = self.serializer(obj)
        res = {
            'code': 1001,
            'msg': '查询成功',
            'data': serializer.data
        }
        return Response(res)

    def put(self, request, pk):
        obj = self.get_object(pk)

        serializer = self.serializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            res = {
                'code': 1001,
                'msg': '修改成功',
                'data': serializer.data
            }
        else:
            res = {
                'code': 1002,
                'msg': '修改失败',
                'data': serializer.data
            }
        return Response(res)

    def patch(self, request, pk):
        obj = self.get_object(pk)

        serializer = self.serializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            res = {
                'code': 1001,
                'msg': '修改成功',
                'data': serializer.data
            }
        else:
            res = {
                'code': 1002,
                'msg': '修改失败',
                'data': serializer.data
            }
        return Response(res)

    def delete(self, request, pk):
        obj = self.get_object(pk)

        obj.is_deleted = True
        obj.save()
        res = {
            'code': 1001,
            'msg': '删除成功',
            'data': None
        }
        return Response(res)

    def post(self, request, pk):
        objects = self.model.objects.filter(team_id=pk)
        serializer = self.serializer(objects, many=True)
        res = {
            'code': 1001,
            'msg': '查询成功',
            'data': serializer.data
        }
        return Response(res)


class SubDetailAPIView(DetailAPIView):
    def post(self, request, pk):
        objects = self.model.objects.filter(project_id=pk)
        serializer = self.serializer(objects, many=True)
        res = {
            'code': 1001,
            'msg': '查询成功',
            'data': serializer.data
        }
        return Response(res)


class ProjectListAPIView(ListAPIView):
    model = Project
    serializer = ProjectModelSerializer


class ProjectDetailAPIView(DetailAPIView):
    model = Project
    serializer = ProjectModelSerializer


class PrototypeListAPIView(ListAPIView):
    model = Prototype
    serializer = PrototypeModelSerializer


class PrototypeDetailAPIView(SubDetailAPIView):
    model = Prototype
    serializer = PrototypeModelSerializer


class UMLListAPIView(ListAPIView):
    model = UML
    serializer = UMLModelSerializer


class UMLDetailAPIView(SubDetailAPIView):
    model = UML
    serializer = UMLModelSerializer


class DocumentListAPIView(ListAPIView):
    model = Document
    serializer = DocumentModelSerializer


class DocumentDetailAPIView(SubDetailAPIView):
    model = Document
    serializer = DocumentModelSerializer
