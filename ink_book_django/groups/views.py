from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import GroupsSerializer, GroupsRelationsSerializer
from .models import Groups, GroupsRelations
from users.serializers import UserSerializer
from utils.secret import *
from users.models import *
from django.db.models import Q
from utils.config import default_file_system
from utils.websocket_utils import send_to_ws

from projects.models import Document, Project
from projects.serializers import DocumentModelSerializer
from json import dumps, loads

import time
import asyncio


class GroupList(APIView):
    def get(self, request):
        groups = Groups.objects.all()
        serializer = GroupsSerializer(groups, many=True)
        return Response({'code': 1001, 'msg': '查询成功', 'data': serializer.data})

    def post(self, request):
        # 序列化团队信息
        serializer = GroupsSerializer(data=request.data)

        # 查询用户
        try:
            user = Users.objects.get(pk=request.data.get("creator"))
        except:
            return Response({'code': 1003, 'msg': '用户不存在', 'data': ''})

        # 查询群组名
        group = Groups.objects.filter(name__exact=request.data.get("name"))
        if group.exists():
            return Response({'code': 1004, 'msg': '群组名已存在', 'data': ''})

        try:
            # 验证数据的合法性
            if serializer.is_valid():
                # 更改用户的目前的群组
                serializer.save()
                cur_group = Groups.objects.filter(name__exact=request.data.get("name"))
                user.cur_group = cur_group[0].id
                user.save()

                # 新建一个和团队绑定的文件
                doc_serializer = DocumentModelSerializer(data={"name": "Readme.md",
                                                               "team_id": serializer.data.get('id')})
                doc_serializer.is_valid()
                doc_serializer.save()

                # 新建文件的聊天室号码
                doc = Document.objects.get(id=doc_serializer.data.get('id'))
                doc.encryption = des_encrypt(str(doc.id) + 'document', "document")
                doc.save()

                # 更改json文件
                group = Groups.objects.get(id=serializer.data.get('id'))
                default_file_system["children"][1]["file_id"] = doc.id
                default_file_system["children"][1]["encryption"] = str(doc.encryption)
                group.file_system = dumps(default_file_system, ensure_ascii=False)
                group.save()

                return Response({'code': 1001, 'msg': '新建成功', 'data': serializer.data})
            else:
                return Response({'code': 1002, 'msg': '新建失败', 'data': serializer.data})
        except Exception as e:
            print(e)
            return Response({'code': 1002, 'msg': '新建失败', 'data': serializer.data})


class UserGroup(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        groups_relations = GroupsRelations.objects.filter(user_id__exact=user_id)
        res = []
        for relation in groups_relations:
            serializer = GroupsSerializer(Groups.objects.get(pk=relation.group_id))
            res.append(serializer.data)
        return Response({'code': 1001, 'msg': '查询成功', 'data': res})


class GroupDetail(APIView):
    def get(self, request, pk):
        try:
            group = Groups.objects.get(pk=pk)
            serializer = GroupsSerializer(group)
            return Response({'code': 1001, 'msg': '查询成功', 'data': serializer.data})
        except:
            return Response({'code': 1002, 'msg': '群组不存在', 'data': ''})

    def patch(self, request, pk):
        try:
            group = Groups.objects.get(pk=pk)
            serializer = GroupsSerializer(group, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'code': 1001, 'msg': '修改成功', 'data': serializer.data})
            return Response({'code': 1002, 'msg': '修改失败', 'data': serializer.data})
        except:
            return Response({'code': 1002, 'msg': '群组不存在', 'data': ''})


class GroupsRelationsDetail(APIView):
    def patch(self, request):
        user_id = request.data.get('user_id')
        group_id = request.data.get('group_id')
        status = request.data.get('status')
        try:
            group = Groups.objects.get(pk=group_id)
            if int(user_id) == group.creator:
                return Response({'code': 1004, 'msg': '无法修改创建者', 'data': ''})
        except:
            return Response({'code': 1003, 'msg': '群组不存在', 'data': ''})
        try:
            relation = GroupsRelations.objects.get(Q(user_id__exact=user_id) & Q(group_id__exact=group_id))
            relation.status = status
            relation.save()
            return Response({'code': 1001, 'msg': '修改成功', 'data': ''})
        except:
            return Response({'code': 1002, 'msg': '更新失败', 'data': ''})

    def delete(self, request):
        user_id = request.data.get('user_id')
        group_id = request.data.get('group_id')
        try:
            relation = GroupsRelations.objects.get(Q(user_id__exact=user_id) & Q(group_id__exact=group_id))
            relation.delete()
            user = Users.objects.get(pk=user_id)
            user.cur_group = user.personal_group
            user.save()
            return Response({'code': 1001, 'msg': '删除成功', 'data': ''})
        except:
            return Response({'code': 1002, 'msg': '删除失败', 'data': ''})


class GroupsRelationsList(APIView):
    def get(self, request):
        groups_relations = GroupsRelations.objects.all()
        serializer = GroupsSerializer(groups_relations, many=True)
        return Response({'code': 1001, 'msg': '查询成功', 'data': serializer.data})

    def post(self, request):
        user_id = request.data.get('user_id')
        group_id = request.data.get('group_id')
        relations = GroupsRelations.objects.filter(Q(user_id__exact=user_id) & Q(group_id__exact=group_id))
        if relations.exists():
            return Response({'code': 1002, 'msg': '已加入该团队', 'data': ''})

        serializer = GroupsRelationsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'code': 1001, 'msg': '新建成功', 'data': serializer.data})
        return Response({'code': 1002, 'msg': '新建失败', 'data': serializer.data})


class Encryption(APIView):
    authentication_classes = []

    def post(self, request):
        data = request.data.get('data')
        return Response({'code': 1001, 'msg': '加密成功', 'data': des_encrypt(data)})


class Decrypt(APIView):
    authentication_classes = []

    def post(self, request):
        data = request.data.get('data')
        try:
            return Response({'code': 1001, 'msg': '解密成功', 'data': des_decrypt(data)})
        except:
            return Response({'code': 1002, 'msg': '解析失败', 'data': ''})


class MemberList(APIView):
    def post(self, request):
        groups_relations = GroupsRelations.objects.filter(group_id__exact=request.data.get('group_id'))
        res = []
        for relation in groups_relations:
            serializer = UserSerializer(Users.objects.get(pk=relation.user_id))
            temp = serializer.data
            temp["status"] = relation.status
            res.append(temp)
        return Response({'code': 1001, 'msg': '查询成功', 'data': res})


class FileSystemDetail(APIView):
    def post(self, request):
        try:
            pk = request.data.get('group_id')
            group = Groups.objects.get(pk=pk)
            tree = request.data.get('tree')

            group.file_system = dumps(tree)
            group.save()

            asyncio.run(send_to_ws(pk, tree))
            return Response({'code': 1001, 'msg': '保存成功', 'data': tree})
        except Exception as e:
            print(e)
            return Response({'code': 1002, 'msg': '团队不存在', 'data': ''})


class FileSystemTree(APIView):
    def post(self, request):
        try:
            group = Groups.objects.get(pk=request.data.get('group_id'))
            return Response({'code': 1001, 'msg': '查询成功', 'data': loads(group.file_system)})
        except Exception as e:
            print(e)
            return Response({'code': 1002, 'msg': '团队不存在', 'data': ''})


class GroupTreeFile(APIView):
    def post(self, request):
        try:
            group_id = request.data.get('group_id')
            project_name = request.data.get('project_name')
            file_name = request.data.get('file_name')


            project = Project.objects.get(Q(team_id__exact=group_id) & Q(name__exact=project_name))


            # 新建一个和团队绑定的文件
            doc_serializer = DocumentModelSerializer(data={"name": file_name,
                                                            "project_id": project.id,
                                                            "team_id": group_id})
            doc_serializer.is_valid()
            doc_serializer.save()

            # 新建文件的聊天室号码
            doc = Document.objects.get(id=doc_serializer.data.get('id'))
            doc.encryption = des_encrypt(str(doc.id) + 'document', "document")
            doc.save()

            # 更改json文件
            group = Groups.objects.get(id=group_id)
            file_system = loads(group.file_system)
            dir_list = file_system["children"]
            for dir in dir_list:
                if dir["name"] == "项目文档区":
                    for project in dir["children"]:
                        if project["name"] == project_name:
                            new_file = {
                                "name": file_name,
                                "id": int(time.time()),
                                "file_id": doc.id,
                                "encryption":str(doc.encryption),
                                "dragDisabled": True,
                                "editNodeDisabled": True,
                                "delNodeDisabled": True,
                                "isLeaf": True
                            }
                            project["children"].append(new_file)
            group.file_system = dumps(file_system, ensure_ascii=False)
            group.save()
            asyncio.run(send_to_ws(group_id, file_system))
            return Response({"code": 1001, "msg": "新建成功", "data": ""})
        except Exception as e:
            print(e)
            return Response({"code": 1002, "msg": "新建失败", "data": ""})


class DocumentCreator(APIView):
    def post(self,request):
        group_id = request.data.get('group_id')
        file_name = request.data.get('file_name')

        # 新建一个和团队绑定的文件
        doc_serializer = DocumentModelSerializer(data={"name": file_name,
                                                       "team_id": group_id})
        doc_serializer.is_valid()
        doc_serializer.save()

        # 新建文件的聊天室号码
        doc = Document.objects.get(id=doc_serializer.data.get('id'))
        doc.encryption = des_encrypt(str(doc.id) + 'document', "document")
        doc.save()

        return  Response({"code": 1001, "msg": "导出成功", "data": DocumentModelSerializer(doc).data})