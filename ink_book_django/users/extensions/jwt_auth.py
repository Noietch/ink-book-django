from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf.global_settings import SECRET_KEY
import jwt
from jwt import exceptions
import datetime


class JwtAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.data.get("token")
        try:
            msg = jwt.decode(token, SECRET_KEY, algorithms="HS256")
            return msg, token
        except exceptions.ExpiredSignatureError:
            raise AuthenticationFailed({"code": 8848, "msg": "token 过期", "data":''})
        except exceptions.DecodeError:
            raise AuthenticationFailed({"code": 8849, "msg": "token 解析错误", "data":''})
        except exceptions.InvalidTokenError:
            raise AuthenticationFailed({"code": 8847, "msg": "token 非法", "data":''})


def create_token(payload, timeout=1440):
    headers = {
        'typ': 'jwt',
        'alg': 'HS256'
    }
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=timeout)
    result = jwt.encode(payload=payload, key=SECRET_KEY, algorithm="HS256", headers=headers)
    return result


if __name__ == '__main__':
    h = create_token({"username":"123123"})
    msg = jwt.decode(h, SECRET_KEY, algorithms="HS256")
    