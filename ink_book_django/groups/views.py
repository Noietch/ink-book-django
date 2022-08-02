from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *


class GroupList(APIView):
    def post(self,request):
        serializer = GroupsSerializer(request.data)


class GroupsRelationsList(APIView):
    def post(self,request):
        serializer = GroupsSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'code': 1001, 'msg': '新建成功', 'data': serializer.data})
        return Response({'code': 1002, 'msg': '新建失败', 'data': serializer.data})


class MemberList(APIView):
    def post(self,request):
        pass