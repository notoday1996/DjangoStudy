import pandas as pd
from pandas.core.frame import DataFrame
import math
import numpy as np
import os


def recommendation_page(stu_id, spark_id, history):
    path = path = os.path.abspath('../DjangoStudy/data_platform/用户预分类.xlsx')
    df = pd.read_excel(path, encoding='utf-8', index_col=False, header=0)
    print(df)

    stu_df = df[df['学号'] == stu_id]
    group_num = stu_df['分组结果'].tolist()[0]

    # ===============获取目标分类的整个组========================
    test = df[df['分组结果'].isin([group_num])]
    a = test['学号']

    # =================查找目标用户的火花ID=======================
    user_list = df[df['学号'].isin(a)]
    spark_id_list = user_list['spark_id']
    spark_id_list = spark_id_list.reset_index(drop=True)
    print(spark_id_list)

    # path2 = path = os.path.abspath('../DjangoStudy/data_platform/wp_history.csv')
    # history = pd.read_csv(path2, encoding='utf-8', index_col=False, header=0)

    # ===================根据群组所有用的ID获取所有的相关的浏览记录========================
    need = history[history['user_id'].isin(spark_id_list)]
    need = need.reset_index(drop=True)
    print(need)

    # =======================获取所有相关页面的ID作为之后dataframe的列名=====================
    all_post_id = need['action_post_id']
    clean_post_id = all_post_id.drop_duplicates(keep='first')
    clean_post_id = clean_post_id.reset_index(drop=True)
    print(clean_post_id)

    # =======================计算目标用户与组内其他用户对于相关页面的浏览情况列表=================
    print(spark_id)
    target_df = history[history['user_id'] == spark_id]
    target_post_id = target_df['action_post_id']
    target_post_id = target_post_id.drop_duplicates()
    # target_post_id = target_post_id.reset_index(drop=True)
    t = target_post_id.tolist()
    print(t)
    target = []
    for i in range(len(clean_post_id)):
        if clean_post_id[i] in t:
            target.append(1)
        else:
            target.append(0)
    # print(target)

    # =========================计算组内其他用户的相关页面浏览列表以及与目标用户的相似性===================
    td = spark_id_list[spark_id_list.values == spark_id].index
    target_index = td[0]  # 由于返回的结果会是一个array是pandas的数据结构所以要用td[0]
    group_member = spark_id_list.drop(target_index)
    group_member_id = group_member.tolist()

    member_list = []
    similarity = []
    for member in group_member_id:
        member_df = history[history['user_id'] == member]
        member_post_id = member_df['action_post_id']
        member_post_id = member_post_id.drop_duplicates()
        # member_post_id = member_post_id.reset_index(drop=True)
        m = member_post_id.tolist()
        member = []
        # print(member_post_id)
        n1 = set(target_post_id) & set(member_post_id)
        n2 = len(set(target_post_id)) * len(set(member_post_id))
        if n2 == 0:
            similarity.append(0)
        else:
            s = len(n1) / math.sqrt(n2)
            similarity.append(s)

        for i in range(len(clean_post_id)):
            if clean_post_id[i] in m:
                member.append(1)
            else:
                member.append(0)
        member_list.append(member)
    # print(member_list)
    # print(similarity)

    # ========================通过相似性和浏览水平，计算需要推荐的页面ID===================
    header = clean_post_id.tolist()
    t = target_post_id.tolist()

    score = []  # 根据相似性计算每个页面的评分
    for i in range(len(member_list)):
        temp = []
        for j in range(len(member_list[i])):
            temp.append(similarity[i] * member_list[i][j])
        score.append(temp)

    collection = DataFrame(score, columns=header)
    # 去除目标用户已经浏览的页面
    c = collection.drop(t, axis=1)

    res = c.sum(axis=0)
    res = res.sort_values(ascending=False)
    # for i in range(10):
    #     print(res[i].index)

    final_res = res.index
    final_res = final_res.tolist()  # 得到最终所有页面ID的评分
    print(final_res[:10])
    return final_res[:10]

