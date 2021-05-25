# Create your views here.
from django.shortcuts import render, redirect

from jinja2 import Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig
from django.http import HttpResponse

CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./demo/templates"))

from pyecharts import options as opts
from pyecharts.charts import Bar

import numpy as np
import pandas as pd
import random
# from .models import chatQdata, senior_sentiment_dictionary, totalStopwords
import re
import nltk
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager
from konlpy.tag import Okt
from pyecharts.charts import Gauge, Page
from pyecharts.charts import Bar
from pyecharts import options as opts
# from __future__ import unicode_literals
import math

from django.http import HttpResponse
from django.template import loader
from pyecharts.charts import Line3D


import pymysql
#
# # conn = pymysql.connect(host='13.209.193.138', port=3306, user='root', passwd='test', db='mariaDB2')
# # cur = conn.cursor()
#
#
# # models.py 에서 생성한 각 class를 불러온다
#


def graph():
    df = pd.read_csv('c:/Temp/Chatterbot_Q.csv', encoding='utf-8')
    df.columns = ["id", 'question']
    sentence_list = [sentence for sentence in df['question']]
    total_stopwords = pd.read_csv('c:/Temp/total_stopwords.csv', encoding='utf-8')
    total_stopwords.columns = ["id", 'stopword']
    total_stopwords = list(np.array(total_stopwords['stopword'].tolist()))
    words = []
    for sentence in sentence_list:
        # sentence = re.sub('([a-zA-Z])', '', sentence)
        # sentence = re.sub("[ㄱ-ㅎㅏ-ㅣ]+", '', sentence)
        # sentence = re.sub(r'[0-9]+', '', sentence)
        # sentence = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', sentence)
        hangul = re.compile('[^ \u3131-\u3163\uac00-\ud7a3]+')
        sentence = hangul.sub('', sentence)
        t = Okt()
        temp = t.morphs(sentence, stem=True, norm=True)
        temp = [word for word in temp if not word in total_stopwords]
        words.append(temp)
    words = [item for sublist in words for item in sublist]
    word_list = [word.replace("고프다", "배고프다") for word in words]
    word_list = [word.replace("배배고프다", "배고프다") for word in word_list]
    word_list = [word.replace("모닝", "아침") for word in word_list]
    word_list = [word.replace("굿", "좋다") for word in word_list]
    word_df = pd.DataFrame(word_list)
    word_df.columns = ['word']
    contains_v = word_df.loc[word_df['word'].str.endswith("다", na=False)]
    verb_list = [verb for verb in contains_v['word']]
    verb_df = pd.DataFrame(pd.DataFrame(verb_list)[0].value_counts())
    verb_df.reset_index(inplace=True)  # 재실행하면 오류주의!
    verb_df.columns = ['word', 'count']
    font_fname = 'C:/jsj/DJANGOexam/project_helper/firstapp/static/fonts/경기천년바탕_Bold.ttf'
    font_family = font_manager.FontProperties(fname=font_fname).get_name()

    plt.rcParams["font.family"] = font_family
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.size'] = 22.
    plt.rcParams['xtick.labelsize'] = 17.
    plt.rcParams['ytick.labelsize'] = 17.
    plt.rcParams['axes.labelsize'] = 17.
    plt.figure(figsize=(10, 8))
    sns.barplot(x='word', y='count', data=verb_df[0:10])
    plt.title('가장 많이 쓰는 표현', fontsize=22)
    plt.xlabel('')
    plt.ylabel('횟수')
    plt.savefig("firstapp/static/images/test.png")

    contains_xv = word_df.loc[-word_df['word'].str.endswith("다", na=False)]
    nonverbal_list = [verb for verb in contains_xv['word']]
    n_df = pd.DataFrame(pd.DataFrame(nonverbal_list)[0].value_counts())
    n_df.reset_index(inplace=True)  # 재실행하면 오류주의!
    n_df.columns = ['word', 'count']
    font_fname = 'C:/jsj/DJANGOexam/project_helper/firstapp/static/fonts/경기천년바탕_Bold.ttf'
    font_family = font_manager.FontProperties(fname=font_fname).get_name()

    plt.rcParams["font.family"] = font_family
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.size'] = 22.
    plt.rcParams['xtick.labelsize'] = 17.
    plt.rcParams['ytick.labelsize'] = 17.
    plt.rcParams['axes.labelsize'] = 17.
    plt.figure(figsize=(10, 8))
    sns.barplot(x='word', y='count', data=n_df[0:10])
    plt.title('가장 많이 쓰는 단어', fontsize=22)
    plt.xlabel('')
    plt.ylabel('횟수')
    plt.savefig("firstapp/static/images/test1.png")

    senior_dic = pd.read_csv('c:/Temp/Senior_sentiment_dictionary.csv')
    list_df = pd.DataFrame(verb_list)
    list_df.columns = ['word']
    df_LEFT_JOIN = pd.merge(list_df, senior_dic, left_on='word', right_on='word', how='left')
    df_LEFT_JOIN['polarity'] = df_LEFT_JOIN['polarity'].fillna(0)
    df_LEFT_JOIN['sentiment'] = df_LEFT_JOIN['sentiment'].fillna("neu")
    # 긍정
    is_pos = df_LEFT_JOIN['sentiment'] == 'pos'
    pos_list = df_LEFT_JOIN[is_pos]
    pos_df = pd.DataFrame(pos_list['word'].value_counts())
    pos_df.reset_index(inplace=True)  # 재실행하면 오류주의!
    pos_df.columns = ['word', 'count']
    font_fname = 'C:/jsj/DJANGOexam/project_helper/firstapp/static/fonts/경기천년바탕_Bold.ttf'
    font_family = font_manager.FontProperties(fname=font_fname).get_name()
    plt.rcParams["font.family"] = font_family
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.size'] = 22.
    plt.rcParams['xtick.labelsize'] = 17.
    plt.rcParams['ytick.labelsize'] = 17.
    plt.rcParams['axes.labelsize'] = 17.
    plt.figure(figsize=(10, 8))
    sns.barplot(x='word', y='count', data=pos_df[0:10])
    plt.title('긍정표현', fontsize=22)
    plt.xlabel('')
    plt.ylabel('횟수')
    plt.savefig("firstapp/static/images/positive.png")

    # 부정
    is_neg = df_LEFT_JOIN['sentiment'] == 'neg'
    neg_list = df_LEFT_JOIN[is_neg]
    neg_df = pd.DataFrame(neg_list['word'].value_counts())
    neg_df.reset_index(inplace=True)  # 재실행하면 오류주의!
    neg_df.columns = ['word', 'count']
    font_fname = 'C:/jsj/DJANGOexam/project_helper/firstapp/static/fonts/경기천년바탕_Bold.ttf'
    font_family = font_manager.FontProperties(fname=font_fname).get_name()
    plt.rcParams["font.family"] = font_family
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.size'] = 22.
    plt.rcParams['xtick.labelsize'] = 17.
    plt.rcParams['ytick.labelsize'] = 17.
    plt.rcParams['axes.labelsize'] = 17.
    plt.figure(figsize=(10, 8))
    sns.barplot(x='word', y='count', data=neg_df[0:10])
    plt.title('부정표현', fontsize=22)
    plt.xlabel('')
    plt.ylabel('횟수')
    plt.savefig("firstapp/static/images/negative.png")


def sg(request):
    graph()
    return render(request, 'chart.html')