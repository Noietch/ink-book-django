import utils.html_content as email_content
from .extensions.jwt_auth import create_token
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from utils.mailsender import MailSender
from utils.random_generator import get_verification_code
from utils.config import email_config, img_path, img_url
from utils.image_utils import image_save
import time
import os


class UserList(APIView):
    authentication_classes = []
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
    def get(self, request, pk):
        try:
            user = Users.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response({'code': 1001, 'msg': '查询成功', 'data': serializer.data})
        except:
            return Response({'code': 1002, 'msg': '用户不存在', 'data': ''})

    def patch(self, request, pk):
        try:
            user = Users.objects.get(pk=pk)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'code': 1001, 'msg': '修改成功', 'data': serializer.data})
            return Response({'code': 1002, 'msg': '修改失败', 'data': serializer.data})
        except:
            return Response({'code': 1003, 'msg': '用户不存在', 'data': ''})


class UserLogin(APIView):
    authentication_classes = []
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = Users.objects.get(username__exact=email)
            serializer = UserSerializer(user)
        except:
            return Response({'code': 1003, 'msg': '用户不存在', 'data': ''})
        cur_user = authenticate(username=email, password=password)
        res = {'id':serializer.data.get('id')}
        if cur_user is not None:
            return Response({'code': 1001, 'msg': '登陆成功', 'data': create_token(res)})
        else:
            return Response({'code': 1002, 'msg': '登陆失败', 'data': ''})


class UserInfo(APIView):
    def post(self, request):
        try:
            user = Users.objects.get(pk=request.user["id"])
            serializer = UserSerializer(user)
            return Response({'code': 1001, 'msg': '查询成功', 'data': serializer.data})
        except:
            return Response({'code': 1002, 'msg': '用户不存在', 'data': ''})


class UserPassword(APIView):
    authentication_classes = []
    def patch(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            user = Users.objects.get(email__exact=email)
            user.set_password(password)
            user.save()
            return Response({'code': 1001, 'msg': '修改成功', 'data': ''})
        except:
            return Response({'code': 1002, 'msg': '用户不存在', 'data': ''})


class EmailVerification(APIView):
    authentication_classes = []
    def post(self, request):
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


class UploadAvatar(APIView):
    authentication_classes = []
    def post(self,request):
        try:
            user_id = request.POST.get('user_id')
            image = request.FILES.get("file")
            extension = os.path.splitext(image.name)[-1]
            filename = "{}{}".format(time.time(),extension)
            path = os.path.join(img_path, filename)
            image_save(image, path)
            url = os.path.join(img_url,filename)
            user = Users.objects.get(pk = user_id)
            user.avatar = url
            user.save()
            return Response({'ret': 1001, 'msg': "上传成功", 'data': url})
        except Exception as e:
            print(e)
            return Response({'ret': 1002, 'msg': "上传失败", 'data': ''})