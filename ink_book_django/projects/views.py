from rest_framework.views import APIView
from rest_framework.response import Response

from .models import *
from .serializers import *


# Create your views here.
class ListAPIView(APIView):
    model = None
    serializer = None

    def get(self, request):
        objects = self.model.objects.all()
        serializer = self.serializer(objects, many=True)
        res = {
            'code': 1001,
            'msg': '查询成功',
            'data': serializer.data
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
            return None
        return obj

    def get(self, request, pk):
        obj = self.get_object(pk)
        if obj is None:
            return Response({
                'code': 1002,
                'msg': '对象不存在',
                'data': None
            })

        serializer = self.serializer(obj)
        res = {
            'code': 1001,
            'msg': '查询成功',
            'data': serializer.data
        }
        return Response(res)

    def put(self, request, pk):
        obj = self.get_object(pk)
        if obj is None:
            return Response({
                'code': 1002,
                'msg': '对象不存在',
                'data': None
            })

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
                'code': 1003,
                'msg': '修改失败',
                'data': serializer.data
            }
        return Response(res)

    def patch(self, request, pk):
        obj = self.get_object(pk)
        if obj is None:
            return Response({
                'code': 1002,
                'msg': '对象不存在',
                'data': None
            })

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
                'code': 1003,
                'msg': '修改失败',
                'data': serializer.data
            }
        return Response(res)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        if obj is None:
            return Response({
                'code': 1002,
                'msg': '对象不存在',
                'data': None
            })

        obj.delete()
        res = {
            'code': 1001,
            'msg': '删除成功',
            'data': None
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


class PrototypeDetailAPIView(DetailAPIView):
    model = Prototype
    serializer = PrototypeModelSerializer


class UMLListAPIView(ListAPIView):
    model = UML
    serializer = UMLModelSerializer


class UMLDetailAPIView(DetailAPIView):
    model = UML
    serializer = UMLModelSerializer


class DocumentListAPIView(ListAPIView):
    model = Document
    serializer = DocumentModelSerializer


class DocumentDetailAPIView(DetailAPIView):
    model = Document
    serializer = DocumentModelSerializer
