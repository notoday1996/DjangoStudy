# 使用jwt进行token的用户鉴权
import datetime
from django.conf import settings
import jwt
from jwt import exceptions


JWT_SALT = settings.SECRET_KEY


def create_token(payload, timeout=20):
    """
    :param payload:  例如：{'user_id':1,'username':'wupeiqi'}用户信息
    :param timeout: token的过期时间，默认20分钟
    :return:
    """
    headers = {
        'typ': 'jwt',
        'alg': 'HS256'
    }
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=timeout)
    result = jwt.encode(payload=payload, key=JWT_SALT, algorithm="HS256", headers=headers).decode('utf-8')
    # result = jwt.encode(payload=payload, key=JWT_SALT, algorithm="HS256", headers=headers)
    return result


def parse_payload(token):
    """
    对token进行和发行校验并获取payload
    :param token:
    :return:
    """
    result = {'status': False, 'data': None, 'error': None}
    try:
        verified_payload = jwt.decode(token, JWT_SALT, algorithm="HS256")
        result['status'] = True
        result['data'] = verified_payload
    except exceptions.ExpiredSignatureError:
        result['error'] = 'token已失效'
    except jwt.DecodeError:
        result['error'] = 'token认证失败'
    except jwt.InvalidTokenError:
        result['error'] = '非法的token'
    return result


def parse_token(token):
    result = False
    verified_token = jwt.decode(token, JWT_SALT, algorithms="HS256")
    return verified_token

