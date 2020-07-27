from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection
import json
import pandas as pd
import datetime
from Report.jwt_token import create_token, parse_payload, parse_token
import hashlib
from Report.models import User
import os
from Report.reommendation import recommendation_page


def hello(request):
    a = "欢迎来到火花空间数据分析平台"
    return HttpResponse(a)


def tokenTest(request):

    token = create_token({'username': 'superAdmin'})
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
                response['tips'] = "注册成功"
            else:
                response['error'] = "两次密码不一致"

    return JsonResponse(response)

# ======================总体情况统计部分=====================


# ===============根据起始和结束时间筛选相应的history======================
def range_history_select(str1, str2):
    start_time = datetime.datetime.strptime(str1, '%Y-%m-%d')
    end_time = datetime.datetime.strptime(str2, '%Y-%m-%d')
    offset = datetime.timedelta(days=1)
    end_time = end_time + offset

    path = path = os.path.abspath('../DjangoStudy/data_platform/wp_history.csv')
    history = pd.read_csv(path, encoding='utf-8', index_col=False, header=0)
    useless_pages = useless_list()
    # =========去除导航页等无效页面===============
    history = history[~history['action_post_id'].isin(useless_pages)]

    history['action_time'] = pd.to_datetime(history['action_time'])
    history['leave_time'] = pd.to_datetime(history['leave_time'])

    range_history = history[(history['action_time'] > start_time) & (history['action_time'] <= end_time)]
    return range_history


def useless_list():
    path = os.path.abspath('../DjangoStudy/data_platform/wp_posts.csv')
    post = pd.read_csv(path, encoding='utf-8', index_col=False, header=0)
    useless = post[post['post_type'] == 'page']
    useless_page = useless['ID'].tolist()
    return useless_page


def posts_select():
    path = path = os.path.abspath('../DjangoStudy/data_platform/wp_posts.csv')
    post = pd.read_csv(path, encoding='utf-8', index_col=False, header=0)
    return post


# ======================根据发送的时间获取相应统计数据=======================
def basic_information(request):
    # ==================读取所有的历史记录=================
    path = path = os.path.abspath('../DjangoStudy/data_platform/wp_history.csv')
    history = pd.read_csv(path, encoding='utf-8', index_col=False, header=0)
    result = {}
    response = {'status': 200, 'data': None, 'error': None}

    result['spark_start_time'] = "2017年5月"
    result['previous_spark'] = "火花空间论坛"
    result['data_nums'] = 57717 + len(history)
    result['serve_student'] = "3000余人"
    result['all_page'] = "11000+"
    result['all_wiki'] = "9500+"
    result['all_project'] = "900+"
    result['all_aq'] = "300+"
    result['update_times'] = "42812次"

    response['data'] = result

    return JsonResponse(response)


def browse_statistic(request):
    if request.method == 'POST':
        start = request.POST.get('startTime')
        end = request.POST.get('endTime')
        range_history = range_history_select(start, end)
        response = {'status': 200, 'data': None, 'error': None}

        time1 = datetime.datetime.now()
        temp = range_history['action_post_id'].value_counts().rename('count').reset_index()
        temp.columns = ['post_id', 'count']
        temp = temp.head(10)
        top = temp['post_id'].tolist()
        nums = temp['count'].tolist()
        time2 = datetime.datetime.now()
        print(time2-time1)

        post = posts_select()
        temp_result = post[post['ID'].isin(top)]
        titles = temp_result['post_title'].tolist()
        guid = temp_result['guid'].tolist()
        print(titles)
        result = {}

        result['post_title'] = titles
        result['count'] = nums
        result['guid'] = guid

        response['data'] = result

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
        response = {'status': 200, 'data': None, 'error': None}

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
        post_title = ret['post_title'].tolist()
        post_url = ret['guid'].tolist()

        result = {}

        result['total_question'] = total_question
        result['total_answer'] = total_answer
        result['hot_qa'] = post_title
        result['url'] = post_url

        response['data'] = result

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
        response = {'status': 200, 'data': None, 'error': None}
        result = {}
        print(time_divide)
        history = range_history_select(start, end)
        print(history)
        nums = []
        for i in range(len(time_divide)-1):
            temp = history[history['action_time'] > time_divide[i]]
            ret = temp[temp['action_time'] <= time_divide[i+1]]
            nums.append(len(ret))
        result['daily_browse'] = nums
        response['data'] = result
        print(response)
        return JsonResponse(response)
# =======================总体情况统计部分结束=========================


# ===================学生个人信息部分======================

# ====================各项基础信息的返回=====================
def student_information(stu_id):
    response = {}

    path = os.path.abspath('../DjangoStudy/data_platform/student_information.xls')
    information = pd.read_excel(path, encoding='utf-8', index_col=False, header=0)
    # print(information)
    stu = information[information['stu_id'] == stu_id]
    print(stu)

    response['two_weeks_ago_browse'] = stu['two_weeks_ago_browse'].tolist()[0]
    response['last_week_browse'] = stu['last_week_browse'].tolist()[0]
    response['talk_QQ'] = stu['talk_QQ'].tolist()[0]
    response['test_score'] = stu['talk_QQ'].tolist()[0]
    response['metacognition'] = stu['metacognition'].tolist()[0]
    response['deal_style'] = stu['deal_style'].tolist()[0]
    response['perception_style'] = stu['perception_style'].tolist()[0]
    response['understand_style'] = stu['understand_style'].tolist()[0]
    response['completion'] = stu['completion'].tolist()[0]
    response['self_evaluation'] = stu['self_evaluation'].tolist()[0]
    return response


def personal_information(request):
    response = {'status': False, 'data': None, 'error': None}
    token = request.META.get('HTTP_AUTHORIZATION')
    print(token)
    verify = parse_payload(token)
    data = verify['data']
    username = data['username']
    print(username)
    user = User.objects.filter(username=username)
    user = user.first()
    stu_id = int(user.stu_id)
    print(stu_id)
    ret = student_information(stu_id)
    if len(ret) != 0:
        response['data'] = ret
        response['status'] = 200

    return JsonResponse(response)


def student_info(request):
    if request.method == 'POST':
        response = {'status': False, 'data': None, 'error': None}
        stu_id = request.POST.get('stu_id')
        stu_id = int(stu_id)
        result = student_information(stu_id)
        if len(result) != 0:
            response['status'] = 200
            response['data'] = result

    return JsonResponse(response)


def student_track_make(start, end, spark_id):
    start_time = datetime.datetime.strptime(start, '%Y-%m-%d')
    end_time = datetime.datetime.strptime(end, '%Y-%m-%d')
    offset = datetime.timedelta(days=1)
    end_time = end_time + offset
    time_divide = pd.date_range(start_time, end_time, freq='24H')

    history = range_history_select(start, end)
    history = history[history['user_id'] == spark_id]
    time_divide = pd.date_range(start_time, end_time, freq='24H')
    nums = []
    for i in range(len(time_divide) - 1):
        temp = history[history['action_time'] > time_divide[i]]
        result = temp[temp['action_time'] <= time_divide[i + 1]]
        nums.append(len(result))

    return nums


def personal_browse_track(request):
    if request.method == 'POST':
        token = request.META.get('HTTP_AUTHORIZATION')
        verify = parse_payload(token)
        response = {'status': False, 'data': None, 'error': None}
        result = {}
        data = verify['data']
        username = data['username']
        user = User.objects.filter(username=username)
        user = user.first()
        spark_id = int(user.spark_id)
        start = request.POST.get('startTime')
        end = request.POST.get('endTime')
        result['daily_browse'] = student_track_make(start, end, spark_id)
        if len(result) != 0:
            response['data'] = result
            response['status'] = 200
        else:
            response['error'] = "token失效或者验证失败"

    return JsonResponse(response)


def student_browse_track(request):
    if request.method == 'POST':
        response = {'status': False, 'data': None, 'error': None}
        result = {}
        stu_id = request.POST.get('stu_id')
        stu_id = int(stu_id)
        start = request.POST.get('startTime')
        end = request.POST.get('endTime')
        path = os.path.abspath('../DjangoStudy/data_platform/student_information.xls')
        information = pd.read_excel(path, encoding='utf-8', index_col=False, header=0)
        student = information[information['stu_id'] == stu_id]
        spark_id = student['spark_id'].tolist()[0]

        result['daily_browse'] = student_track_make(start, end, spark_id)
        if len(result) != 0:
            response['status'] = 200
            response['data'] = result

    return JsonResponse(response)


# ==通过数据归一化处理，把几个维度得分转化为0-1的范围，通过雷达图对比==
def compare_radar(request):
    # 几个维度分别为，浏览量、发言量、最新的元认知水平、教程的完成度、最新一次的小测成绩、自我评价
    if request.method == 'POST':
        response = {'status': False, 'data': [], 'error': None}
        token = request.META.get('HTTP_AUTHORIZATION')
        print(token)
        verify = parse_payload(token)
        result = {}
        data = verify['data']
        username = data['username']
        user = User.objects.filter(username=username)
        user = user.first()
        me_id = int(user.stu_id)
        # me_id = user.stu_id
        compare_id = request.POST.get('stu_id')
        compare_id = int(compare_id)
        me = student_information(me_id)
        compare = student_information(compare_id)
        print(len(me))
        print(len(compare))

        if len(me) != 0 and len(compare) != 0:
            result['me'] = me
            result['compare'] = compare
            response['data'] = result
            response['status'] = 200

        else:
            response['error'] = "token无效或者过期"

    return JsonResponse(response)


# ======================学生个人信息部分结束========================

# =========================基于用户预分类结果的学习内容推荐======================
def recommendation(request):
    if request.method == 'POST':
        response = {'status': False, 'data': [], 'error': None}
        result = {}
        token = request.META.get('HTTP_AUTHORIZATION')
        verify = parse_payload(token)
        data = verify['data']
        username = data['username']
        user = User.objects.filter(username=username)
        user = user.first()
        stu_id = int(user.stu_id)
        spark_id = int(user.spark_id)
        print(stu_id)

        start = request.POST.get('startTime')
        end = request.POST.get('endTime')
        history = range_history_select(start, end)

        recommendation_pages = recommendation_page(stu_id, spark_id, history)
        # recommendation_pages = map(eval, recommendation_pages)
        print(recommendation_pages)
        if len(recommendation_pages) != 0:
            posts = posts_select()
            recommendation_list = posts[posts['ID'].isin(recommendation_pages)]
            print(recommendation_list)
            title = recommendation_list['post_title'].tolist()
            print(title)
            url = recommendation_list['guid'].tolist()
            result['title'] = title
            result['url'] = url
            response['data'] = result
            response['status'] = 200

    return JsonResponse(response)








