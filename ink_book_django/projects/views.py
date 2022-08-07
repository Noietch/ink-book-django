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

    def validate(self, serializer):
        team_id = serializer.validated_data['team_id']
        name = serializer.validated_data['name']
        return not self.model.objects.filter(team_id=team_id, name=name).exists()

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
            if not self.validate(serializer):
                res = {
                    'code': 1003,
                    'msg': '命名重复',
                    'data': serializer.data
                }
            else:
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


class SubListAPIView(ListAPIView):
    def validate(self, serializer):
        project_id = serializer.validated_data['project_id']
        name = serializer.validated_data['name']
        return not self.model.objects.filter(project_id=project_id, name=name).exists()


class DetailAPIView(APIView):
    model = None
    serializer = None

    def validate(self, obj, serializer):
        try:
            team_id = serializer.validated_data['team_id']
        except:
            team_id = obj.team_id
        try:
            name = serializer.validated_data['name']
        except:
            name = obj.name
        return not (self.model.objects.filter(team_id=team_id, name=name).exists()
            and not self.model.objects.get(team_id=team_id, name=name) == obj)

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
            if not self.validate(None, serializer):
                res = {
                    'code': 1004,
                    'msg': '命名重复',
                    'data': serializer.data
                }
            else:
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
            if not self.validate(obj, serializer):
                res = {
                    'code': 1004,
                    'msg': '命名重复',
                    'data': serializer.data
                }
            else:
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
    def validate(self, obj, serializer):
        try:
            project_id = serializer.validated_data['project_id']
        except:
            project_id = obj.project_id
        try:
            name = serializer.validated_data['name']
        except:
            name = obj.name
        return not (self.model.objects.filter(project_id=project_id, name=name).exists()
                and not self.model.objects.get(project_id=project_id, name=name) == obj)

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

    def copy(self, request, pk):
        obj = self.get_object(pk)
        if obj is None:
            return Response({
                'code': 1002,
                'msg': '对象不存在',
                'data': None
            })
        
        name = obj.name
        old_serializer = ProjectModelSerializer(obj)
        data = old_serializer.data
        data['name'] = '%s_copy' % name
        new_serializer = ProjectModelSerializer(data=old_serializer.data)
        if serializer.is_valid():
            count = 2
            while not self.validate(obj, serializer):
                new_serializer.validated_data['name'] = '%s_copy%d' % (name, count)
                count += 1
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


class PrototypeListAPIView(SubListAPIView):
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

        serializer = self.serializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            if not self.validate(obj, serializer):
                res = {
                    'code': 1004,
                    'msg': '命名重复',
                    'data': serializer.data
                }
            else:
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


class PrototypeInfoAPIView(APIView):
    def post(self, request):
        try:
            obj = Prototype.objects.get(id=request.data.get('id'))
        except Prototype.DoesNotExist:
            return Response({
                'code': 1002,
                'msg': '对象不存在',
                'data': None
            })
        serializer = PrototypeModelSerializer(obj)
        res = {
            'code': 1001,
            'msg': '查询成功',
            'data': serializer.data
        }
        return Response(res)


class UMLListAPIView(SubListAPIView):
    model = UML
    serializer = UMLModelSerializer


class UMLDetailAPIView(SubDetailAPIView):
    model = UML
    serializer = UMLModelSerializer


class DocumentListAPIView(SubListAPIView):
    model = Document
    serializer = DocumentModelSerializer

    def post(self, request):
        serializer = DocumentModelSerializer(data=request.data)
        if serializer.is_valid():
            if not self.validate(serializer):
                res = {
                    'code': 1003,
                    'msg': '命名重复',
                    'data': serializer.data
                }
            else:
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
