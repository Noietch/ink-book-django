import utils.html_content as email_content
from extensions.jwt_auth import create_token
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from django.http import Http404
from utils.mailsender import MailSender
from utils.random_generator import get_verification_code
from utils.config import email_config


class UserList(APIView):
    def get(self, request):
        users = Users.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({'code': 1001, 'msg': '查询成功', 'data': serializer.data})

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        cur_user = Users.objects.filter(username__exact=email)
        if cur_user.exists():
            return Response({'code': 1002, 'msg': '用户名已存在', 'data': ''})
        new_user = Users.objects.create_user(username=email, email=email, password=password)
        new_user.save()
        serializer = UserSerializer(new_user)
        return Response({'code': 1001, 'msg': '注册成功', 'data': serializer.data})


class UserDetail(APIView):
    def get_object(self, pk):
        try:
            return Users.objects.get(pk=pk)
        except Users.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response({'code': 1001, 'msg': '查询成功', 'data': serializer.data})

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'code': 1001, 'msg': '修改成功', 'data': serializer.data})
        return Response({'code': 1002, 'msg': '修改失败', 'data': serializer.data})

    def patch(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'code': 1001, 'msg': '修改成功', 'data': serializer.data})
        return Response({'code': 1002, 'msg': '修改失败', 'data': serializer.data})


class UserLogin(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = Users.objects.get(username__exact=email)
            serializer = UserSerializer(user)
        except:
            return Response({'code': 1003, 'msg': '用户已存在', 'data': ''})
        cur_user = authenticate(username=email, password=password)
        if cur_user is not None:
            return Response({'code': 1001, 'msg': '修改成功', 'data': create_token(serializer.data)})
        else:
            return Response({'code': 1002, 'msg': '修改失败', 'data': create_token(serializer.data)})


class UserInfo(APIView):
    def post(self, request):
        return Response({'code': 1001, 'msg': '查询成功', 'data': request.user})


class UserPassword(APIView):
    def get_object(self, pk):
        try:
            return Users.objects.get(pk=pk)
        except Users.DoesNotExist:
            raise Http404

    def patch(self, request, pk):
        user = self.get_object(pk)
        password = request.data.get('password')
        user.set_password(password)
        user.save()
        return Response({'code': 1001, 'msg': '修改成功', 'data': ''})


class EmailVerification(APIView):
    def get(self, request):
        sender = email_config["email_sender"]
        receiver = request.data.get("email")
        authority_code = email_config["authority_code"]
        m = MailSender(sender, receiver, authority_code)
        code = get_verification_code()
        rep = m.send_html("验证码", email_content.content.format(code))
        if rep:
            return Response({'ret': 1001, 'msg': "发送成功", 'data': code})
        else:
            return Response({'ret': 1002, 'msg': "发送失败", 'data': ''})
