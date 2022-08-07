from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from json import loads, dumps
from django.db.models import Model

from .models import *
from .serializers import *
from groups.models import GroupsRelations
from utils.secret import *
from utils.config import *
from utils.image_utils import base64_image

import pdfkit
import time
import os

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

    def post(self, request, pk):
        try:
            search_key = request.data['search']
        except:
            search_key = ""
        try:
            sort_key = request.data['sort']
        except:
            sort_key = 'id'
        try:
            order = request.data['desc']
        except:
            order = 1
        objects1 = Project.objects.filter(team_id=pk, name__contains=search_key, is_deleted=False).order_by(sort_key)
        objects2 = Project.objects.filter(team_id=pk, name__contains=search_key, is_deleted=True).order_by(sort_key)
        serializer1 = PrototypeModelSerializer(objects1, many=True)
        serializer2 = PrototypeModelSerializer(objects2, many=True)
        if order == 1:
            data = [serializer1.data, serializer2.data]
        elif order == 2:
            data = [serializer1.data.__reversed__(), serializer2.data.__reversed__()]
        else:
            return Response({'code': 1002, 'msg': '排序错误', 'data': None})
        res = {
            'code': 1001,
            'msg': '查询成功',
            'data': data
        }
        return Response(res)


class ProjectCopyAPIView(APIView):
    def validate(self, serializer):
        team_id = serializer.validated_data['team_id']
        name = serializer.validated_data['name']
        return not Project.objects.filter(team_id=team_id, name=name).exists()

    def copy(self, obj, model, serializer, validate):
        old_serializer = serializer(obj)
        name = obj.name
        data = old_serializer.data
        data['name'] = '%s_copy' % name
        new_serializer = serializer(data=data)

        if new_serializer.is_valid():
            count = 2
            while not self.validate(new_serializer):
                new_serializer.validated_data['name'] = '%s_copy%d' % (name, count)
                count += 1
            new_serializer.save()
            return new_serializer.data
        else:
            return None

    def sub_copy(self, obj, serializer, fk):
        old_serializer = serializer(obj)
        data = old_serializer.data
        data['project_id'] = fk
        new_serializer = serializer(data=data)

        if new_serializer.is_valid():
            new_serializer.save()
            return True
        else:
            return False

    def get_object(self, pk):
        try:
            obj = Project.objects.get(id=pk)
        except Project.DoesNotExist:
            obj = None
        return obj

    def post(self, request):
        pk = request.data.get('id')
        obj = self.get_object(pk)
        if obj is None:
            return Response({
                'code': 1002,
                'msg': '对象不存在',
                'data': None
            })
        res = {
            'code': 1003,
            'msg': '复制失败',
            'data': None
        }
        data = self.copy(obj, Project, ProjectModelSerializer, self.validate)
        if data is None:
            return Response(res)

        Models = [Prototype, UML, Document]
        Serializers = [PrototypeModelSerializer, UMLModelSerializer, DocumentModelSerializer]
        for i in range(0, 3):
            for obj in Models[i].objects.filter(project_id=pk):
                if not self.sub_copy(obj, Serializers[i], data['id']):
                    return Response(res)

        res = {
            'code': 1001,
            'msg': '复制成功',
            'data': data
        }
        return Response(res)


class PrototypeListAPIView(SubListAPIView):
    model = Prototype
    serializer = PrototypeModelSerializer

    def get(self, request):
        objects1 = self.model.objects.filter(is_deleted=False)
        serializer1 = self.serializer(objects1, many=True)
        # for data in serializer1.data:
        #     try:
        #         data['components'] = loads(loads(data['components']))
        #     except:
        #         pass
        objects2 = self.model.objects.filter(is_deleted=True)
        serializer2 = self.serializer(objects2, many=True)
        # for data in serializer2.data:
        #     try:
        #         data['components'] = loads(loads(data['components']))
        #     except:
        #         pass
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
        # for data in serializer1.data:
        #     try:
        #         data['components'] = loads(loads(data['components']))
        #     except:
        #         pass
        objects2 = self.model.objects.filter(project_id=pk, is_deleted=True)
        serializer2 = self.serializer(objects2, many=True)
        # for data in serializer2.data:
        #     try:
        #         data['components'] = loads(loads(data['components']))
        #     except:
        #         pass
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


class PrototypeUserAPIView(APIView):
    authentication_classes = []
    def post(self, request):
        user_id = request.data.get('user_id')
        prototype_id = request.data.get('prototype_id')
        if user_id is None:
            prototype = Prototype.objects.get(id=prototype_id)
            return Response({
                'code': 1001,
                'msg': '查询成功',
                'data': prototype.public
            })

        else:
            try:
                group_id = Project.objects.get(id=Prototype.objects.get(id=prototype_id).project_id).team_id
            except Model.DoesNotExist:
                return Response({'code': 1002, 'msg': '查询失败', 'data': None})
            return Response({
                'code': 1001,
                'msg': '查询成功',
                'data': GroupsRelations.objects.filter(user_id=user_id, group_id=group_id).exists()
            })


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


class DocumentCenterAPIView(APIView):
    def post(self, request, pk):
        res = {"name": "documentMall", "label": "文档中心", "icon": "user", "url": "UserManage/UserManage"}
        projects_all = []
        for project in Project.objects.filter(team_id=pk):
            pro_dict = {"name": project.name, "label": "project"}
            labels = []
            for label in Document.LABELS:
                label_dict = {"name": label, "label": "group"}
                documents_labels = []
                documents = Document.objects.filter(project_id=project.id, label=label)
                for document in documents:
                    documents_labels.append(document.get_info())
                label_dict['children'] = documents_labels
                labels.append(label_dict)
            pro_dict['children'] = labels
            projects_all.append(pro_dict)
        res['children'] = projects_all
        return Response({'code': 1001, 'msg': '查询成功', 'data': res})



class PDFConvertor(APIView):
    def post(self, request):
        try:
            filename = request.data.get('name')
            content = request.data.get('content')
            full_name = filename + str(time.time()) + '.pdf'
            path = os.path.join(img_path, full_name)
            pdfkit.from_string(content, path)
            return Response({"code": 1001, "msg": "导出成功", "data": os.path.join(img_url, full_name)})
        except Exception as e:
            print("PDFConvertor:", e)
            return Response({"code": 1002, "msg": "导出失败", "data": ''})


class ImageUpload(APIView):
    def post(self, request):
        try:
            img = request.data.get('img')
            full_name = str(time.time()) + ".jpg"
            path = os.path.join(img_path, full_name)
            base64_image(img, path)
            return Response({"code": 1001, "msg": "导出成功", "data": os.path.join(img_url, full_name)})
        except Exception as e:
            print("ImageUpload:", e)
            return Response({"code": 1002, "msg": "导出失败", "data": ''})