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
        serializer.is_valid(raise_exception=True)
        serializer.save()
        res = {
            'code': 1001,
            'msg': '添加成功',
            'data': serializer.validated_data
        }
        return Response(res)


class DetailAPIView(APIView):
    model = None
    serializer = None

    def get(self, request, pk):
        try:
            object = self.model.objects.get(id=pk)
        except self.model.DoesNotExist:
            return Response({
                'code': 1002,
                'msg': '对象不存在',
                'data': None
                })

        serializer = self.serializer(instance=object)
        res = {
            'code': 1001,
            'msg': '查询成功',
            'data': serializer.data
        }
        return Response(res)

    def put(self, request, pk):
        try:
            object = self.model.objects.get(id=pk)
        except self.model.DoesNotExist:
            return Response({
                'code': 1002,
                'msg': '对象不存在',
                'data': None
            })

        serializer = self.serializer(instance=object, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        res = {
            'code': 1001,
            'msg': '修改成功',
            'data': serializer.data
        }
        return Response(res)

    def delete(self, request, pk):
        try:
            object = self.model.objects.get(id=pk)
        except self.model.DoesNotExist:
            return Response({
                'code': 1002,
                'msg': '对象不存在',
                'data': None
            })

        object.delete()
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


class DocumentListAPIView(ListAPIView):
    model = Document
    serializer = DocumentModelSerializer


class DocumentDetailAPIView(DetailAPIView):
    model = Document
    serializer = DocumentModelSerializer
