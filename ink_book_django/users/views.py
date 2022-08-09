from .extensions.jwt_auth import create_token
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import Users

from utils.mailsender import MailSender
from utils.random_generator import get_verification_code
from utils.config import *
from utils.secret import *
from utils.image_utils import image_save
import utils.html_content as email_content

from groups.models import Groups,GroupsRelations
from projects.serializers import DocumentModelSerializer
from projects.models import Document

from json import dumps
import time
import os


class UserList(APIView):
    authentication_classes = []

    def get(self, request):
        users = Users.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({'code': 1001, 'msg': '查询成功', 'data': serializer.data})

    def post(self, request):
        try:
            email = request.data.get("email")
            password = request.data.get("password")

            # 查询用户是否存在
            cur_user = Users.objects.filter(username__exact=email)
            if cur_user.exists():
                return Response({'code': 1002, 'msg': '用户名已存在', 'data': ''})

            # 创建新用户
            new_user = Users.objects.create_user(username=email, email=email, password=password)
            new_user.save()

            # 给用户创建属于自己的团队
            user = Users.objects.filter(username__exact=email)[0]
            group = Groups.objects.create(name=email, creator=user.id)
            group.save()

            # 让用户加入自己的团队
            group_id = Groups.objects.filter(name=email, creator=user.id)[0].id
            group_relations = GroupsRelations.objects.create(user_id=user.id, group_id=group_id, status="管理员")
            group_relations.save()

            # 设置用户目前的团队和个人团队号就是自己的团队
            user.cur_group = group_id
            user.personal_group = group_id
            user.save()

            # 返回用户的信息
            serializer = UserSerializer(user)

            # 新建一个和团队绑定的文件
            doc_serializer = DocumentModelSerializer(data={"name": "Readme.md",
                                                           "team_id": group_id})
            doc_serializer.is_valid()
            doc_serializer.save()

            # 新建文件的聊天室号码
            doc = Document.objects.get(id=doc_serializer.data.get('id'))
            doc.encryption = des_encrypt(str(doc.id) + 'document', "document")
            doc.save()

            # 更改json文件
            group = Groups.objects.get(id=group_id)
            default_file_system["children"][1]["file_id"] = doc.id
            default_file_system["children"][1]["encryption"] = str(doc.encryption)
            group.file_system = dumps(default_file_system, ensure_ascii=False)
            group.save()

            return Response({'code': 1001, 'msg': '注册成功', 'data': serializer.data})
        except Exception as e:
            print(e)
            return Response({'code': 1001, 'msg': '注册失败', 'data': ''})


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
        res = {'id': serializer.data.get('id')}
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

    def post(self, request):
        try:
            user_id = request.POST.get('user_id')
            image = request.FILES.get("file")
            extension = os.path.splitext(image.name)[-1]
            filename = "{}{}".format(time.time(), extension)
            path = os.path.join(img_path, filename)
            image_save(image, path)
            url = os.path.join(img_url, filename)
            user = Users.objects.get(pk=user_id)
            user.avatar = url
            user.save()
            return Response({'ret': 1001, 'msg': "上传成功", 'data': url})
        except Exception as e:
            print(e)
            return Response({'ret': 1002, 'msg': "上传失败", 'data': ''})
