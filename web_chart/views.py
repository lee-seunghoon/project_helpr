# Create your views here.
from django.shortcuts import render, redirect

import numpy as np
import pandas as pd
from .models import chatQdata,  senior_sentiment_dictionary, totalStopwords
import re
import nltk
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager
from konlpy.tag import Okt
# models.py 에서 생성한 각 class를 불러온다

def graph1(request):
    chatData_df = pd.DataFrame(list(chatQdata.objects.all().values()))
    stopwords_df = pd.DataFrame(list(totalStopwords.objects.all().values()))
    # 각 class에서 pandas로 데이터 뽑아오기
    chatData_df.columns = ['id', 'question']
    stopwords_df.columns = ['id', 'stopword']
    chatData_df = chatData_df['question']
    stopwords_df = stopwords_df['stopword']
    df = pd.DataFrame(chatData_df[['question']].str.strip())
    df.columns = ['question']
    sentence_list = list(np.array(df['question'].tolist()))
    total_stopwords = list(np.array(stopwords_df['stopword'].tolist()))
    t = Okt()
    X_train = []
    for sentence in sentence_list:
        sentence = re.sub('([a-zA-Z])', '', sentence)
        sentence = re.sub('[ㄱ-ㅎㅏ-ㅣ]+', '', sentence)
        sentence = re.sub(r'[0-9]+', '', sentence)
        sentence = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', sentence)
        hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
        sentence = hangul.sub('', sentence)
        temp_X = t.morphs(sentence, stem=True, norm=True)
        temp_X = [word for word in temp_X if not word in total_stopwords]
        X_train.append(temp_X)
    X_train = [item for sublist in X_train for item in sublist]
    word_list = [word.replace("고프다", "배고프다") for word in X_train]
    word_list = [word.replace("배배고프다", "배고프다") for word in word_list]
    word_list = [word.replace("모닝", "아침") for word in word_list]
    word_list = [word.replace("굿", "좋다") for word in word_list]
    word_df = pd.DataFrame(word_list)
    word_df.columns = ['word']
    contains_동사 = word_df.loc[word_df['word'].str.endswith("다", na=False)]
    contains_동사[['word']]
    verb_list = [verb for verb in contains_동사['word']]
    verb_df = pd.DataFrame(pd.DataFrame(verb_list)[0].value_counts())
    verb_df.reset_index(inplace=True)  # 재실행하면 오류주의!
    verb_df.columns = ['word', 'count']

    font_fname = 'C:/jsj/DJANGOexam/project_helper/firstapp/static/fonts/경기천년바탕_Bold.ttf'
    font_family = font_manager.FontProperties(fname=font_fname).get_name()

    plt.rcParams["font.family"] = font_family
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.size'] = 13.
    plt.rcParams['xtick.labelsize'] = 11.
    plt.rcParams['ytick.labelsize'] = 11.
    plt.rcParams['axes.labelsize'] = 13.
    plt.figure(figsize=(5, 2))
    sns.barplot(x='word', y='count', data=verb_df[0:15])
    plt.title('가장 많이 쓰는 표현')
    plt.savefig('C:/jsj/DJANGOexam/project_helper/firstapp/static/images/The_most_used_expressions.png')
    return render(request, 'chart.html')


def graph2(request):
    chatData_df = pd.DataFrame(list(chatQdata.objects.all().values()))
    stopwords_df = pd.DataFrame(list(totalStopwords.objects.all().values()))
    # 각 class에서 pandas로 데이터 뽑아오기
    chatData_df.columns = ['id', 'question']
    chatData_df = chatData_df['question']
    stopwords_df = stopwords_df['stopword']
    df = pd.DataFrame(chatData_df['question'].str.strip())
    df.columns = ['question']
    sentence_list = list(np.array(df['question'].tolist()))
    total_stopwords = list(np.array(stopwords_df['stopword'].tolist()))
    t = Okt()
    X_train = []
    for sentence in sentence_list:
        sentence = re.sub('([a-zA-Z])', '', sentence)
        sentence = re.sub('[ㄱ-ㅎㅏ-ㅣ]+', '', sentence)
        sentence = re.sub(r'[0-9]+', '', sentence)
        sentence = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', sentence)
        hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
        sentence = hangul.sub('', sentence)
        temp_X = t.morphs(sentence, stem=True, norm=True)
        temp_X = [word for word in temp_X if not word in total_stopwords]
        X_train.append(temp_X)
    X_train = [item for sublist in X_train for item in sublist]
    word_list = [word.replace("고프다", "배고프다") for word in X_train]
    word_list = [word.replace("배배고프다", "배고프다") for word in word_list]
    word_list = [word.replace("모닝", "아침") for word in word_list]
    word_list = [word.replace("굿", "좋다") for word in word_list]
    word_df = pd.DataFrame(word_list)
    word_df.columns = ['word']
    contains_동사제외 = word_df.loc[-word_df['word'].str.endswith("다", na=False)]
    No_verb_list = [verb for verb in contains_동사제외['word']]
    No_verb_df = pd.DataFrame(pd.DataFrame(No_verb_list)[0].value_counts())
    No_verb_df.reset_index(inplace=True)  # 재실행하면 오류주의!
    No_verb_df.columns = ['word', 'count']
    import matplotlib.pyplot as plt
    from matplotlib import font_manager

    font_fname = 'C:/jsj/DJANGOexam/project_helper/firstapp/static/fonts/경기천년바탕_Bold.ttf'
    font_family = font_manager.FontProperties(fname=font_fname).get_name()

    plt.rcParams["font.family"] = font_family
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.size'] = 13.
    plt.rcParams['xtick.labelsize'] = 11.
    plt.rcParams['ytick.labelsize'] = 11.
    plt.rcParams['axes.labelsize'] = 13.
    plt.figure(figsize=(4, 2))
    sns.barplot(x='word', y='count', data=No_verb_df[0:15])
    plt.title('가장 많이 쓰는 단어')
    plt.savefig('C:/jsj/DJANGOexam/project_helper/firstapp/static/images/The_most_used_words.png')
    return render(request, 'chart.html')

def pos_chart(request):
    Senior_dic = pd.DataFrame(list(senior_sentiment_dictionary.objects.all().values()))
    chatData_df = pd.DataFrame(list(chatQdata.objects.all().values()))
    stopwords_df = pd.DataFrame(list(totalStopwords.objects.all().values()))
    # 각 class에서 pandas로 데이터 뽑아오기
    chatData_df.columns = ['id', 'question']
    chatData_df = chatData_df[['question']]
    df = pd.DataFrame(chatData_df['question'].str.strip())
    df.columns = ['question']
    sentence_list = list(np.array(df['question'].tolist()))
    total_stopwords = list(np.array(stopwords_df['stopword'].tolist()))
    t = Okt()
    X_train = []
    for sentence in sentence_list:
        sentence = re.sub('([a-zA-Z])', '', sentence)
        sentence = re.sub('[ㄱ-ㅎㅏ-ㅣ]+', '', sentence)
        sentence = re.sub(r'[0-9]+', '', sentence)
        sentence = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', sentence)
        hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
        sentence = hangul.sub('', sentence)
        temp_X = t.morphs(sentence, stem=True, norm=True)
        temp_X = [word for word in temp_X if not word in total_stopwords]
        X_train.append(temp_X)
    X_train = [item for sublist in X_train for item in sublist]
    word_list = [word.replace("고프다", "배고프다") for word in X_train]
    word_list = [word.replace("배배고프다", "배고프다") for word in word_list]
    word_list = [word.replace("모닝", "아침") for word in word_list]
    word_list = [word.replace("굿", "좋다") for word in word_list]
    word_df = pd.DataFrame(word_list)
    word_df.columns = ['word']
    contains_동사 = word_df.loc[word_df['word'].str.endswith("다", na=False)]
    contains_동사[['word']]
    verb_list = [verb for verb in contains_동사['word']]
    list_df = pd.DataFrame(verb_list)
    df_LEFT_JOIN = pd.merge(list_df, Senior_dic, left_on='word', right_on='word', how='left')
    df_LEFT_JOIN['polarity'] = df_LEFT_JOIN['polarity'].fillna(0)
    df_LEFT_JOIN['sentiment'] = df_LEFT_JOIN['sentiment'].fillna("neu")

    # 긍정
    is_pos = df_LEFT_JOIN['sentiment'] == 'pos'
    pos_list = df_LEFT_JOIN[is_pos]
    pos_df = pd.DataFrame(pos_list['word'].value_counts())
    pos_df.reset_index(inplace=True)  # 재실행하면 오류주의!
    pos_df.columns = ['word', 'count']
    import matplotlib.pyplot as plt
    from matplotlib import font_manager

    font_fname = 'C:/jsj/DJANGOexam/project_helper/firstapp/static/fonts/경기천년바탕_Bold.ttf'
    font_family = font_manager.FontProperties(fname=font_fname).get_name()

    plt.rcParams["font.family"] = font_family
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.size'] = 20.
    plt.rcParams['xtick.labelsize'] = 15.
    plt.rcParams['ytick.labelsize'] = 15.
    plt.rcParams['axes.labelsize'] = 18.
    plt.figure(figsize=(6, 4))
    sns.barplot(x='word', y='count', data=pos_df[0:10])
    plt.title('긍정표현')
    plt.savefig('C:/jsj/DJANGOexam/project_helper/firstapp/static/images/Top_10_positive_words.png')


    return render(request, 'chart.html')

def neg_chart(request):
    Senior_dic = pd.DataFrame(list(senior_sentiment_dictionary.objects.all().values()))
    chatData_df = pd.DataFrame(list(chatQdata.objects.all().values()))
    stopwords_df = pd.DataFrame(list(totalStopwords.objects.all().values()))
    # 각 class에서 pandas로 데이터 뽑아오기
    chatData_df.columns = ['id', 'question']
    chatData_df = chatData_df[['question']]
    df = pd.DataFrame(chatData_df['question'].str.strip())
    df.columns = ['question']
    sentence_list = list(np.array(df['question'].tolist()))
    total_stopwords = list(np.array(stopwords_df['stopword'].tolist()))
    t = Okt()
    X_train = []
    for sentence in sentence_list:
        sentence = re.sub('([a-zA-Z])', '', sentence)
        sentence = re.sub('[ㄱ-ㅎㅏ-ㅣ]+', '', sentence)
        sentence = re.sub(r'[0-9]+', '', sentence)
        sentence = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', sentence)
        hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
        sentence = hangul.sub('', sentence)
        temp_X = t.morphs(sentence, stem=True, norm=True)
        temp_X = [word for word in temp_X if not word in total_stopwords]
        X_train.append(temp_X)
    X_train = [item for sublist in X_train for item in sublist]
    word_list = [word.replace("고프다", "배고프다") for word in X_train]
    word_list = [word.replace("배배고프다", "배고프다") for word in word_list]
    word_list = [word.replace("모닝", "아침") for word in word_list]
    word_list = [word.replace("굿", "좋다") for word in word_list]
    word_df = pd.DataFrame(word_list)
    word_df.columns = ['word']
    contains_동사 = word_df.loc[word_df['word'].str.endswith("다", na=False)]
    contains_동사[['word']]
    verb_list = [verb for verb in contains_동사['word']]
    list_df = pd.DataFrame(verb_list)
    df_LEFT_JOIN = pd.merge(list_df, Senior_dic, left_on='word', right_on='word', how='left')
    df_LEFT_JOIN['polarity'] = df_LEFT_JOIN['polarity'].fillna(0)
    df_LEFT_JOIN['sentiment'] = df_LEFT_JOIN['sentiment'].fillna("neu")

    # 부정
    is_neg = df_LEFT_JOIN['sentiment'] == 'neg'
    neg_list = df_LEFT_JOIN[is_neg]
    neg_df = pd.DataFrame(neg_list['word'].value_counts())
    neg_df.reset_index(inplace=True)  # 재실행하면 오류주의!
    neg_df.columns = ['word', 'count']
    import matplotlib.pyplot as plt
    import matplotlib.pyplot as plt
    from matplotlib import font_manager

    font_fname = 'C:/jsj/DJANGOexam/project_helper/firstapp/static/fonts/경기천년바탕_Bold.ttf'
    font_family = font_manager.FontProperties(fname=font_fname).get_name()

    plt.rcParams["font.family"] = font_family
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.size'] = 20.
    plt.rcParams['xtick.labelsize'] = 15.
    plt.rcParams['ytick.labelsize'] = 15.
    plt.rcParams['axes.labelsize'] = 18.
    plt.figure(figsize=(6, 4))
    sns.barplot(x='word', y='count', data=neg_df[0:10])
    plt.title('부정표현')
    plt.savefig('C:/jsj/DJANGOexam/project_helper/firstapp/static/images/Top_10_negative_words.png')

    return render(request, 'chart.html')