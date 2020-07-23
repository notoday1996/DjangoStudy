from django.utils.deprecation import MiddlewareMixin
from Report.jwt_token import parse_payload
from django.http import HttpResponse


class AuthToken(MiddlewareMixin):
    white_list = ['/login', '/register' ]  # 白名单

    def process_request(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        print(token)
        verify = parse_payload(token)
        url = request.path_info
        print(url)
        print(verify['status'])

        if url in self.white_list:
            return
        elif verify['status']:
            return
        else:
            return HttpResponse("token验证失败123")

