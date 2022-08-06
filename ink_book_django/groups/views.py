from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from users.serializers import UserSerializer
from utils.secret import *
from users.models import *
from django.db.models import Q

class GroupList(APIView):
    def get(self, request):
        groups = Groups.objects.all()
        serializer = GroupsSerializer(groups, many=True)
        return Response({'code': 1001, 'msg': '查询成功', 'data': serializer.data})

    def post(self, request):
        serializer = GroupsSerializer(data=request.data)
        try:
            user = Users.objects.get(pk = request.data.get("creator"))
        except:
            return Response({'code': 1003, 'msg': '用户不存在', 'data': ''})

        group = Groups.objects.filter(name__exact = request.data.get("name"))
        if group.exists():
            return Response({'code': 1004, 'msg': '群组名已存在', 'data': ''})

        try:
            if serializer.is_valid():
                serializer.save()
                cur_group = Groups.objects.get(name__exact = request.data.get("name"))
                user.cur_group = cur_group.id
                return Response({'code': 1001, 'msg': '新建成功', 'data': serializer.data})
            return Response({'code': 1002, 'msg': '新建失败', 'data': serializer.data})
        except:
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
    def patch(self,request):
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

    def delete(self,request):
        user_id = request.data.get('user_id')
        group_id = request.data.get('group_id')
        try:
            relation = GroupsRelations.objects.get(Q(user_id__exact=user_id) & Q(group_id__exact=group_id))
            relation.delete()
            try:
                user = Users.objects.get(pk = user_id)
                if user.cur_group == group_id:
                    if GroupsRelations.objects.filter(user_id__exact=user_id).exists():
                        relation = GroupsRelations.objects.filter(user_id__exact=user_id)[0]
                        user.cur_group = relation.group_id
                    else:
                        user.cur_group = 0
            except:
                pass
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
    def post(self, request):
        data = request.data.get('data')
        return Response({'code': 1001, 'msg': '加密成功', 'data': des_encrypt(data)})


class Decrypt(APIView):
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
