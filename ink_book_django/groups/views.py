from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from users.serializers import UserSerializer
from django.http import Http404
from utils.secret import *
from users.models import *


class GroupList(APIView):
    def get(self, request):
        groups = Groups.objects.all()
        serializer = GroupsSerializer(groups, many=True)
        return Response({'code': 1001, 'msg': '查询成功', 'data': serializer.data})

    def post(self, request):
        serializer = GroupsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'code': 1001, 'msg': '新建成功', 'data': serializer.data})
        return Response({'code': 1002, 'msg': '新建失败', 'data': serializer.data})


class GroupDetail(APIView):
    def get_object(self, pk):
        try:
            return Groups.objects.get(pk=pk)
        except Groups.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        group = self.get_object(pk)
        serializer = GroupsSerializer(group)
        return Response({'code': 1001, 'msg': '查询成功', 'data': serializer.data})

    def patch(self, request, pk):
        group = self.get_object(pk)
        serializer = GroupsSerializer(group, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'code': 1001, 'msg': '修改成功', 'data': serializer.data})
        return Response({'code': 1002, 'msg': '修改失败', 'data': serializer.data})


class GroupsRelationsList(APIView):
    def get(self, request):
        groups_relations = GroupsRelations.objects.all()
        serializer = GroupsSerializer(groups_relations, many=True)
        return Response({'code': 1001, 'msg': '查询成功', 'data': serializer.data})

    def post(self, request):
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
        return Response({'code': 1001, 'msg': '解密成功', 'data': des_decrypt(data)})


class MemberList(APIView):
    def get(self, request, pk):
        groups_relations = GroupsRelations.objects.filter(group_id__exact=pk)
        res = []
        for relation in groups_relations:
            serializer = UserSerializer(Users.objects.get(pk=relation.user_id))
            temp = serializer.data
            temp["status"] = relation.status
            res.append(temp)
        return Response({'code': 1001, 'msg': '查询成功', 'data': res})