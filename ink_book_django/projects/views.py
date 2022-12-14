from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Model
from django.db.models import Q

from .models import Project, Prototype, UML, Document, StarProject
from .serializers import ProjectModelSerializer, PrototypeModelSerializer, UMLModelSerializer, DocumentModelSerializer, \
    StarProjectModelSerializer
from groups.models import *
from utils.secret import *
from utils.config import *
from utils.image_utils import base64_image
from utils.websocket_utils import send_to_ws
from json import dumps, loads
from pdf2docx import Converter
from html2text import HTML2Text

import pdfkit
import time
import os
import asyncio
import copy

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
            return True
        return not self.model.objects.filter(team_id=team_id, name=name).exists()

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
            return True
        return not self.model.objects.filter(project_id=project_id, name=name).exists()

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

    def post(self, request):
        serializer = ProjectModelSerializer(data=request.data)

        if serializer.is_valid():
            if not self.validate(serializer):
                return Response({'code': 1002, 'msg': '项目已存在', 'data': ''})

            serializer.save()
            group = Groups.objects.get(id=serializer.data.get('team_id'))
            file_system = loads(group.file_system)

            dir_list = file_system["children"]
            for dir in dir_list:
                if dir["name"] == "项目文档区":
                    new_dir = {
                        "name": serializer.data.get('name'),
                        "id": int(time.time()*1000),
                        "isLeaf": False,
                        "isProject": True,
                        "dragDisabled": True,
                        "addTreeNodeDisabled": True,
                        "addLeafNodeDisabled": False,
                        "editNodeDisabled": True,
                        "delNodeDisabled": True,
                        "children": []
                    }
                    dir["children"].append(new_dir)
            group.file_system = dumps(file_system, ensure_ascii=False)
            group.save()
            asyncio.run(send_to_ws(serializer.data.get('team_id'), file_system))
            return Response({'code': 1001, 'msg': '新建成功', 'data': serializer.data})
        return Response({'code': 1002, 'msg': '新建失败', 'data': serializer.data})


class ProjectDetailAPIView(DetailAPIView):
    model = Project
    serializer = ProjectModelSerializer

    def post(self, request, pk):
        try:
            search_key = request.data['search']
        except:
            search_key = ''
        try:
            sort_key = request.data['sort']
        except:
            sort_key = 'id'
        try:
            order = request.data['desc']
        except:
            order = 2
        objects1 = Project.objects.filter(team_id=pk, name__contains=search_key, is_deleted=False).order_by(sort_key)
        objects2 = Project.objects.filter(team_id=pk, name__contains=search_key, is_deleted=True).order_by(sort_key)
        serializer1 = ProjectModelSerializer(objects1, many=True)
        serializer2 = ProjectModelSerializer(objects2, many=True)
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

    def delete(self, request, pk):
        try:
            obj = self.get_object(pk)
            if obj is None:
                return Response({
                    'code': 1002,
                    'msg': '对象不存在',
                    'data': None
                })

            # 编辑树
            team_id = obj.team_id
            groups = Groups.objects.get(id=team_id)
            tree = loads(groups.file_system)

            dir_list = tree["children"]
            for dir in dir_list:
                if dir["name"] == "项目文档区":
                    to_del = None
                    for project_ele in dir["children"]:
                        if project_ele["name"] == obj.name:
                            to_del = project_ele
                            break
                    dir["children"].remove(to_del)
            groups.file_system = dumps(tree,ensure_ascii=False)
            groups.save()

            asyncio.run(send_to_ws(team_id, tree))

            obj.delete()
            for star in StarProject.objects.filter(project_id=pk):
                star.delete()

            res = {
                'code': 1001,
                'msg': '删除成功',
                'data': None
            }
            return Response(res)
        except:
            return Response({
                'code': 1002,
                'msg': '删除失败',
                'data': None
            })


class ProjectRename(APIView):
    def post(self, request):
        try:
            project_id = request.data.get('project_id')
            new_name = request.data.get('new_name')

            project = Project.objects.get(id=project_id)
            

            groups = Groups.objects.get(id=project.team_id)
            tree = loads(groups.file_system)

            dir_list = tree["children"]
            for dir in dir_list:
                if dir["name"] == "项目文档区":
                    for project_ele in dir["children"]:
                        if project_ele["name"] == project.name:
                            project_ele["name"] = new_name
                            break
                            
            groups.file_system = dumps(tree, ensure_ascii=False)
            groups.save()

            asyncio.run(send_to_ws(project.team_id, tree))

            project.name = new_name
            project.save()

            return Response({"code": 1001, "msg": "修改成功", "data": ""})
        except Exception as e:
            print(e)
            return Response({"code": 1001, "msg": "修改成功", "data": ""})



class ProjectCopyAPIView(APIView):
    resource = {}

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
        if isinstance(obj, Document):
            # 记录原文档信息
            old_id = data['id']
            old_encryption = data['encryption']
            # 修改新文档信息
            data['cow'] = 1
        new_serializer = serializer(data=data)

        if new_serializer.is_valid():
            new_serializer.save()
            if isinstance(obj, Document):
                new_id = new_serializer.data['id']
                new_obj = Document.objects.get(id=new_id)
                new_encryption = str(des_encrypt(str(new_id) + 'document', "document"))
                new_obj.encryption = new_encryption
                new_obj.save()
                # 保存字典信息
                self.resource[old_id] = new_id
                self.resource[old_encryption] = new_encryption
            elif isinstance(obj, Prototype):
                new_id = new_serializer.data['id']
                new_obj = Prototype.objects.get(id=new_id)
                new_encryption = str(des_encrypt(str(new_id)))[2:-1]
                new_obj.encryption = new_encryption
                new_obj.save()
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
        self.resource = {}
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

        # 找到所属团队
        old_project = self.get_object(pk)
        team = Groups.objects.get(pk=old_project.team_id)
        tree = loads(team.file_system)
        dir_list = tree["children"]

        new_dir = None
        # 找到那个节点
        for dir in dir_list:
            if dir["name"] == "项目文档区":
                for project_ele in  dir["children"]:
                    if project_ele["name"] == old_project.name:
                        new_dir = copy.deepcopy(project_ele)
                        break

        new_dir["name"] = data['name']
        # 更新节点
        for file in new_dir["children"]:
            file["file_id"] = self.resource[file["file_id"]]
            file["encryption"] = self.resource[file["encryption"]]

        new_dir["id"] = int(time.time()*1000)
        for i in range(len(new_dir["children"])):
            new_dir["children"][i]["id"] = new_dir["id"] + i + 1

        for dir in dir_list:
            if dir["name"] == "项目文档区":
                dir["children"].append(new_dir)

        team.file_system = dumps(tree,ensure_ascii=False)
        team.save()

        asyncio.run(send_to_ws(team.id, tree))

        res = {
            'code': 1001,
            'msg': '复制成功',
            'data': data
        }
        return Response(res)


class ProjectStarListAPIView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        project_id = request.data.get('project_id')
        if StarProject.objects.filter(Q(user_id__exact=user_id) & Q(project_id__exact=project_id)).exists():
            return Response({'code': 1002, 'msg': '已收藏该项目', 'data': None})
        else:
            serializer = StarProjectModelSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'code': 1001, 'msg': '收藏成功', 'data': serializer.data})
            else:
                return Response({'code': 1003, 'msg': '收藏失败', 'data': serializer.data})

    def delete(self, request):
        user_id = request.data.get('user_id')
        project_id = request.data.get('project_id')
        if not StarProject.objects.filter(Q(user_id__exact=user_id) & Q(project_id__exact=project_id)).exists():
            return Response({'code': 1002, 'msg': '未收藏该项目', 'data': None})
        else:
            star = StarProject.objects.get(Q(user_id__exact=user_id) & Q(project_id__exact=project_id))
            star.delete()
            return Response({'code': 1001, 'msg': '删除成功', 'data': None})


class ProjectStarPostAPIView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        team_id = int(request.data.get('group_id'))
        data = []
        for star in StarProject.objects.filter(user_id=user_id):
            try:
                obj = Project.objects.get(Q(id=star.project_id) & Q(is_deleted=False))
            except Project.DoesNotExist:
                continue
            if obj.team_id == team_id:
                serializer = ProjectModelSerializer(obj)
                data.append(serializer.data)
        return Response({'code': 1001, 'msg': '查询成功', 'data': data})


class PrototypeListAPIView(SubListAPIView):
    model = Prototype
    serializer = PrototypeModelSerializer

    def get(self, request):
        objects1 = Prototype.objects.filter(is_deleted=False)
        serializer1 = PrototypeModelSerializer(objects1, many=True)
        objects2 = Prototype.objects.filter(is_deleted=True)
        serializer2 = PrototypeModelSerializer(objects2, many=True)
        res = {'code': 1001, 'msg': '查询成功', 'data': [serializer1.data, serializer2.data]}
        return Response(res)

    def post(self, request):
        try:
            serializer = PrototypeModelSerializer(data=request.data)
            if serializer.is_valid():
                if not self.validate(serializer):
                    res = {'code': 1003, 'msg': '命名重复', 'data': serializer.data}
                else:
                    serializer.save()
                    # 加密
                    obj = Prototype.objects.get(id=serializer.data['id'])
                    obj.encryption = str(des_encrypt(str(obj.id)))[2:-1]
                    # 设置模板内容
                    template = request.data.get('template')
                    if template is not None and template != "" and template > 0:
                        try:
                            template = prototype_template_choices[template]
                            file_path = os.path.join(template_path, prototype_template, template + ".json")
                            with open(file_path) as file:
                                obj.components = file.read()
                        except Exception as e:
                            print(e)
                    obj.save()
                    serializer = PrototypeModelSerializer(obj)
                    res = {'code': 1001, 'msg': '添加成功', 'data': serializer.data}
            else:
                res = {'code': 1002, 'msg': '添加失败', 'data': serializer.data}
            return Response(res)
        except Exception as e:
            print(e)
            return Response({'code': 1002, 'msg': '添加失败', 'data': None})


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


class PrototypeByProjectAPIView(APIView):
    authentication_classes = []

    def post(self, request, pk):
        objects1 = Prototype.objects.filter(project_id=pk, is_deleted=False)
        serializer1 = PrototypeModelSerializer(objects1, many=True)
        objects2 = Prototype.objects.filter(project_id=pk, is_deleted=True)
        serializer2 = PrototypeModelSerializer(objects2, many=True)
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
    authentication_classes = []
    model = UML
    serializer = UMLModelSerializer


class UMLDetailAPIView(SubDetailAPIView):
    authentication_classes = []
    model = UML
    serializer = UMLModelSerializer


class UMLInfoAPIView(APIView):
    authentication_classes = []

    def post(self, request):
        try:
            obj = UML.objects.get(id=request.data.get('id'))
        except UML.DoesNotExist:
            return Response({
                'code': 1002,
                'msg': '对象不存在',
                'data': None
            })
        serializer = UMLModelSerializer(obj)
        res = {
            'code': 1001,
            'msg': '查询成功',
            'data': serializer.data
        }
        return Response(res)


class DocumentListAPIView(SubListAPIView):
    model = Document
    serializer = DocumentModelSerializer

    def post(self, request):
        try:
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

                    # 对于话题信息进行加密
                    obj = Document.objects.get(id=serializer.data['id'])
                    obj.encryption = des_encrypt(str(obj.id) + 'document', "document")

                    # 设置文档模板
                    template = request.data.get('template')
                    if template is not None and template > 0:
                        try:
                            template = document_template_choices[template]
                            file_path = os.path.join(template_path, document_template, template + ".txt")
                            with open(file_path) as file:
                                obj.content = file.read()
                                obj.cow = 1
                        except Exception as e:
                            print(e)
                    obj.save()
                    serializer = DocumentModelSerializer(instance=obj)

                    # 修改文件中心目录结构
                    project = Project.objects.get(id=serializer.data.get('project_id'))
                    group = Groups.objects.get(id=project.team_id)

                    # 修改树形结构
                    file_system = json.loads(group.file_system)
                    dir_list = file_system["children"]
                    for dir in dir_list:
                        if dir["name"] == "项目文档区":
                            for project_ele in dir["children"]:
                                if project_ele["name"] == project.name:
                                    new_file = {
                                        "name": obj.name,
                                        "id": int(time.time()*1000),
                                        "file_id": obj.id,
                                        "encryption": str(obj.encryption),
                                        "dragDisabled": True,
                                        "editNodeDisabled": False,
                                        "delNodeDisabled": False,
                                        "isLeaf": True
                                    }
                                    if not "children" in project_ele:
                                        project_ele["children"] = []
                                    project_ele["children"].append(new_file)

                    group.file_system = json.dumps(file_system, ensure_ascii=False)
                    group.save()
                    asyncio.run(send_to_ws(serializer.data.get('team_id'), file_system))

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
        except Exception as e:
            print(e)
            return Response({
                    'code': 1002,
                    'msg': '添加失败',
                    'data': serializer.data
                })


class DocumentDetailAPIView(SubDetailAPIView):
    model = Document
    serializer = DocumentModelSerializer

    # project_id and team_id
    def validate(self, obj, serializer):
        try:
            project_id = serializer.validated_data['project_id']
        except:
            project_id = obj.project_id
        try:
            team_id = serializer.validated_data['team_id']
        except:
            team_id = obj.team_id
        try:
            name = serializer.validated_data['name']
        except:
            return True
        return not self.model.objects.filter(Q(team_id=team_id) & Q(project_id=project_id) & Q(name=name)).exists()

    def delete(self, request, pk):
        try:
            document = Document.objects.get(pk=pk)

            project = Project.objects.get(id=document.project_id)
            groups = Groups.objects.get(id=document.team_id)

            tree = loads(groups.file_system)
            for dir in tree["children"]:
                if dir["name"] == "文档中心":
                    for pro in dir["children"]:
                        if pro["name"] == project.name:
                            to_del = None
                            for file in pro["children"]:
                                if file["file_id"] == document.id:
                                    to_del = file
                                    break
                            pro["children"].remove(to_del)
            groups.file_system = dumps(tree,ensure_ascii=False)
            groups.save()

            asyncio.run(send_to_ws(document.team_id, tree))

            if document.online_users != 0:
                return Response({'code': 1002, 'msg': '文档正在被编辑', 'data': ''})
            document.delete()
            return Response({'code': 1001, 'msg': '删除成功', 'data': ''})
        except Exception as e:
            print(e)
            return Response({'code': 1003, 'msg': '文档不存在', 'data': ''})


class DocumentDir(APIView):
    def post(self, request):
        group_id = request.data.get('group_id')
        target_id = int(request.data.get('dir_id'))

        group = Groups.objects.get(id=group_id)
        tree = loads(group.file_system)

        # 找到要查询的那个目录
        target_dir = None
        stack = [tree]
        while len(stack) > 0:
            cur_node = stack.pop()
            if cur_node["isLeaf"] == False:
                if cur_node["id"] == target_id:
                    target_dir = cur_node
                    break
                for node in cur_node["children"]:
                    stack.append(node)

        # 查询是否有文件在编辑
        stack = [target_dir]
        while len(stack) > 0:
            cur_node = stack.pop()
            if cur_node["isLeaf"] == True:
                file_id = int(cur_node["file_id"])
                document = Document.objects.get(pk=file_id)
                if document.online_users > 0:
                    return Response({'code': 1002, 'msg': '文件夹中文档正在被编辑', 'data': ''})
            else:
                for node in cur_node["children"]:
                    stack.append(node)

        return Response({'code': 1001, 'msg': '无人编辑', 'data': ''})


class DocumentFile(APIView):
    def post(self, request):
        try:
            document = Document.objects.get(id=request.data.get('file_id'))
            if document.online_users > 0:
                return Response({'code': 1002, 'msg': '文档正在被编辑', 'data': ''})
            return Response({'code': 1001, 'msg': '无人编辑', 'data': ''})
        except:
            return Response({'code': 1003, 'msg': '文件不存在', 'data': ''})


class DocumentInfoAPIView(APIView):
    def post(self, request):
        try:
            obj = Document.objects.get(id=request.data.get('id'))
        except Document.DoesNotExist:
            return Response({
                'code': 1002,
                'msg': '对象不存在',
                'data': None
            })
        serializer = DocumentModelSerializer(obj)
        res = {
            'code': 1001,
            'msg': '查询成功',
            'data': serializer.data
        }
        return Response(res)


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


class FileConvertor(APIView):
    def post(self, request):
        filename = request.data.get('name')
        content = request.data.get('content')
        form = request.data.get('format')

        if form == "pdf":
            try:

                full_name = filename + str(time.time()) + '.pdf'
                path = os.path.join(img_path, full_name)
                pdfkit.from_string(content, path)
                return Response({"code": 1001, "msg": "导出成功", "data": os.path.join(img_url, full_name)})
            except Exception as e:
                print("PDFConvertor:", e)
                return Response({"code": 1002, "msg": "导出失败", "data": ''})

        if form == "md":
            try:
                filename = request.data.get('name')
                content = request.data.get('content')
                full_name = filename + str(time.time()) + '.md'
                # 处理内容
                text = HTML2Text().handle(content)
                # 写入处理后的内容
                path = os.path.join(img_path, full_name)
                with open(path, 'w', encoding='UTF-8') as f:
                    f.write(text)
                return Response({"code": 1001, "msg": "导出成功", "data": os.path.join(img_url, full_name)})
            except Exception as e:
                print("MDConvertor:", e)
                return Response({"code": 1002, "msg": "导出失败", "data": ''})

        if form == "docx":
            try:
                filename = request.data.get('name')
                content = request.data.get('content')
                full_name = filename + str(time.time()) + '.pdf'
                path = os.path.join(img_path, full_name)
                pdfkit.from_string(content, path)
                cv = Converter(path)

                full_name = filename + str(time.time()) + '.docx'
                path = os.path.join(img_path, full_name)
                cv.convert(path)
                cv.close()
                return Response({"code": 1001, "msg": "导出成功", "data": os.path.join(img_url, full_name)})
            except Exception as e:
                print("WordConvertor:", e)
                return Response({"code": 1002, "msg": "导出失败", "data": ''})

        return Response({"code": 1002, "msg": "导出失败", "data": ''})


class ImageUpload(APIView):
    def post(self, request):
        try:
            img = request.data.get('img')
            full_name = str(time.time()) + ".jpg"
            path = os.path.join(img_path, full_name)
            base64_image(img, path)
            data = os.path.join(img_url, full_name)

            prototype_id = request.data.get('prototype_id')
            prototype = Prototype.objects.get(id=prototype_id)
            prototype.img_path = data
            prototype.save()
            return Response({"code": 1001, "msg": "导出成功", "data": data})
        except Exception as e:
            print("ImageUpload:", e)
            return Response({"code": 1002, "msg": "导出失败", "data": ''})
