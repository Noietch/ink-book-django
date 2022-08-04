from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from json import loads, dumps

from .models import *
from .serializers import *
from utils.secret import *


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
            obj = None
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

    def post(self, request, pk):
        objects1 = self.model.objects.filter(team_id=pk, is_deleted=False)
        serializer1 = self.serializer(objects1, many=True)
        objects2 = self.model.objects.filter(team_id=pk, is_deleted=True)
        serializer2 = self.serializer(objects2, many=True)
        res = {
            'code': 1001,
            'msg': '查询成功',
            'data': [serializer1.data, serializer2.data]
        }
        return Response(res)


class SubDetailAPIView(DetailAPIView):
    def post(self, request, pk):
        objects1 = self.model.objects.filter(project_id=pk, is_deleted=False)
        serializer1 = self.serializer(objects1, many=True)
        objects2 = self.model.objects.filter(project_id=pk, is_deleted=True)
        serializer2 = self.serializer(objects2, many=True)
        res = {
            'code': 1001,
            'msg': '查询成功',
            'data': [serializer1.data, serializer2.data]
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

    def get(self, request):
        objects1 = self.model.objects.filter(is_deleted=False)
        serializer1 = self.serializer(objects1, many=True)
        for data in serializer1.data:
            try:
                data['components'] = loads(loads(data['components']))
            except:
                pass
        objects2 = self.model.objects.filter(is_deleted=True)
        serializer2 = self.serializer(objects2, many=True)
        for data in serializer2.data:
            try:
                data['components'] = loads(loads(data['components']))
            except:
                pass
        res = {
            'code': 1001,
            'msg': '查询成功',
            'data': [serializer1.data, serializer2.data]
        }
        return Response(res)


class PrototypeDetailAPIView(SubDetailAPIView):
    model = Prototype
    serializer = PrototypeModelSerializer

    def get(self, request, pk):
        obj = self.get_object(pk)
        if obj is None:
            return Response({
                'code': 1002,
                'msg': '对象不存在',
                'data': None
            })

        serializer = self.serializer(obj)
        data = serializer.data
        try:
            data['components'] = loads(data['components'])
        except:
            pass
        res = {
            'code': 1001,
            'msg': '查询成功',
            'data': data
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

        try:
            data = {'components': dumps(request.data['components'])}
        except:
            data = request.data
        serializer = self.serializer(obj, data=data, partial=True)
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

    def post(self, request, pk):
        objects1 = self.model.objects.filter(project_id=pk, is_deleted=False)
        serializer1 = self.serializer(objects1, many=True)
        for data in serializer1.data:
            try:
                data['components'] = loads(loads(data['components']))
            except:
                pass
        objects2 = self.model.objects.filter(project_id=pk, is_deleted=True)
        serializer2 = self.serializer(objects2, many=True)
        for data in serializer2.data:
            try:
                data['components'] = loads(loads(data['components']))
            except:
                pass
        res = {
            'code': 1001,
            'msg': '查询成功',
            'data': [serializer1.data, serializer2.data]
        }
        return Response(res)


class UMLListAPIView(ListAPIView):
    model = UML
    serializer = UMLModelSerializer


class UMLDetailAPIView(SubDetailAPIView):
    model = UML
    serializer = UMLModelSerializer


class DocumentListAPIView(ListAPIView):
    model = Document
    serializer = DocumentModelSerializer

    def post(self, request):
        serializer = DocumentModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            obj = Document.objects.get(id=serializer.data['id'])
            obj.encryption = des_encrypt(str(obj.id) + '-' + str(obj.project_id), "document")
            obj.save()
            serializer = DocumentModelSerializer(instance=obj)
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


class DocumentDetailAPIView(SubDetailAPIView):
    model = Document
    serializer = DocumentModelSerializer
