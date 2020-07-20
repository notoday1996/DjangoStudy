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


# ===============根据起始和结束时间筛选相应的history======================
def range_history_select(str1, str2):
    start_time = datetime.datetime.strptime(str1, '%Y-%m-%d')
    end_time = datetime.datetime.strptime(str2, '%Y-%m-%d')
    offset = datetime.timedelta(days=1)
    end_time = end_time + offset
    cursor = connection.cursor()
    cursor.execute("select * from history")
    data = cursor.fetchall()
    history = pd.DataFrame(list(data))
    history.columns = ['ID', 'user_id', 'user_action', 'action_post_id', 'action_post_type', 'action_time',
                       'leave_time', 'ip']
    history['action_time'] = pd.to_datetime(history['action_time'])
    history['leave_time'] = pd.to_datetime(history['leave_time'])

    range_history = history[(history['action_time'] > start_time) & (history['action_time'] <= end_time)]
    return range_history


def posts_select():
    cursor = connection.cursor()
    cursor.execute("select * from wp_posts")
    data = cursor.fetchall()
    post = pd.DataFrame(list(data))
    post.columns = ['ID', 'post_author', 'post_date', 'post_date_gmt', 'post_content', 'post_title',
                    'post_excerpt', 'post_status', 'comment_status', 'ping_status', 'post_password', 'post_name',
                    'to_ping', 'pinged', 'post_modified', 'post_modified_gmt', 'post_content_filtered',
                    'post_parent', 'guid', 'menu_order', 'post_type', 'post_mime_type', 'comment_type']
    return post


# ======================根据发送的时间获取相应统计数据=======================
def browse_statistic(request):
    if request.method == 'POST':
        start = request.POST.get('startTime')
        end = request.POST.get('endTime')
        range_history = range_history_select(start, end)
        response = {}

        temp = range_history['action_post_id'].value_counts().rename('count').reset_index()
        temp.columns = ['post_id', 'count']
        temp = temp.head(10)
        top = temp['post_id'].tolist()
        nums = temp['count'].tolist()

        post = posts_select()
        temp_result = post[post['ID'].isin(top)]
        result = temp_result['post_title'].tolist()
        print(result)

        response['post_title'] = result
        response['count'] = nums

        return JsonResponse(response)


def qa_statistic(request):
    if request.method == 'POST':
        start = request.POST.get('startTime')
        end = request.POST.get('endTime')
        range_history = range_history_select(start, end)
        range_history = range_history.drop_duplicates(keep='first')
        range_history = range_history.reset_index(drop=True)
        posts_list = range_history['action_post_id'].tolist()
        post = posts_select()
        temp = post[post['ID'].isin(posts_list)]
        question = temp[temp['post_type'] == 'dwqa-question']
        answer = temp[temp['post_type'] == 'dwqa-answer']
        response = {}

        total_question = len(question)
        total_answer = len(answer)

        q_list = question['ID'].tolist()
        a_list = answer['ID'].tolist()
        qa = q_list + a_list

        all_history = range_history_select(start, end)
        qa_list = all_history[all_history['action_post_id'].isin(qa)]
        qa_list = qa_list['action_post_id'].value_counts().rename('count').reset_index()
        qa_list.columns = ['post_id', 'count']
        qa_list = qa_list.head(10)
        print(qa_list)
        top_qa = qa_list['post_id'].tolist()

        ret = post[post['ID'].isin(top_qa)]
        result = ret['post_title'].tolist()

        response['total_question'] = total_question
        response['total_answer'] = total_answer
        response['hot_qa'] = result

        return JsonResponse(response)


def browse_track(request):
    if request.method == 'POST':
        start = request.POST.get('startTime')
        end = request.POST.get('endTime')
        start_time = datetime.datetime.strptime(start, '%Y-%m-%d')
        end_time = datetime.datetime.strptime(end, '%Y-%m-%d')
        offset = datetime.timedelta(days=1)
        end_time = end_time + offset
        time_divide = pd.date_range(start_time, end_time, freq='24H')
        response = {}
        print(time_divide)
        history = range_history_select(start, end)
        print(history)
        nums = []
        for i in range(len(time_divide)-1):
            temp = history[history['action_time'] > time_divide[i]]
            temp = history[history['action_time'] <= time_divide[i+1]]
            nums.append(len(temp))
        response['daily_browse'] = nums
        return JsonResponse(response)




