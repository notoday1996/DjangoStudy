from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.db import connection
import json
import pandas as pd
import datetime
from Report.jwt_token import create_token, parse_payload, parse_token
import hashlib
from Report.models import User


def book_detail(request, book_id):
    text = "您的图书ID是 %s" % book_id
    return HttpResponse(text)


def author_detail(request):
    author_id = request.GET.get('id')
    text = "这个作者的id是： %s" % author_id
    return HttpResponse(text)


def hello(request):
    a = "返回"
    data ={
        'aaa': a,
    }
    return HttpResponse(json.dumps(data), content_type='application/json')


def tokenTest(request):

    token = create_token({'username': 'testAccount'})
    de_token = parse_payload(token)
    print(token)

    # return HttpResponse(json.dumps(token), content_type='application/json, charset=utf-8')
    return HttpResponse(json.dumps(token))


# =====================注册登入部分的逻辑===============
def passwordTest(request):
    password = "testaccount123"
    if isinstance(password, str):
        password = password.encode('utf-8')
    pwd = hashlib.md5(password).hexdigest().upper()
    return HttpResponse(pwd)


def login(request):
    if request.method == 'POST':
        print("the POST method")
        response = {}
        username = request.POST.get('username')
        pwd = request.POST.get('password')
        md5 = hashlib.md5()
        md5.update(pwd.encode('utf-8'))
        password = md5.hexdigest().upper()
        user = User.objects.filter(username=username)
        if user.count():
            user = user.first()
            if user.password == password:
                token = create_token({'username': username})
                response['status'] = 200
                response['token'] = token
                print("登入成功")
            else:
                response['error'] = "密码错误"
                print("密码错误")
        else:
            response['error'] = "用户不存在"
            print("用户不存在")
        # print(response)
    return HttpResponse(json.dumps(response))


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pwd1 = request.POST.get('password1')
        pwd2 = request.POST.get('password2')
        spark_id = request.POST.get('spark_id')
        stu_id = request.POST.get('stu_id')
        email = request.POST.get('email')
        response = {}

        if User.objects.filter(username=username):
            response['error'] = "该账号已存在"
            print("该账号已存在")
        else:
            if pwd1 == pwd2:
                md5 = hashlib.md5()
                md5.update(pwd1.encode('utf-8'))
                password = md5.hexdigest().upper()
                User.objects.create(username=username, password=password, spark_id=spark_id, stu_id=stu_id, email=email, privilege=1)
                print("注册成功")
                response['status'] = 20000
            else:
                response['error'] = "两次密码不一致"

    return HttpResponse(json.dumps(response))


def basic_information(request):
    # ==================读取所有的历史记录=================
    cursor = connection.cursor()
    cursor.execute("select * from history")
    data = cursor.fetchall()
    df = pd.DataFrame(list(data))
    result = {}

    result['spark_start_time'] = "2017年5月"
    result['previous_spark'] = "火花空间论坛"
    result['data_nums'] = 57717 + len(df)
    result['serve_student'] = "3000余人"
    result['all_page'] = "11000+"
    result['all_wiki'] = "9500+"
    result['all_project'] = "900+"
    result['all_aq'] = "300+"
    result['update_times'] = "42812次"

    return JsonResponse(result)


def save(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        verified_token = parse_token(token)
        username = verified_token['username']




