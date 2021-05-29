import logging

from django.conf import settings
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
import os
import requests
from django.http import HttpResponse
import pymysql
import datetime
import pandas as pd
import requests
from gtts import gTTS

logger = logging.getLogger(__name__)



# 최저,최고온도 함수
def MaxMinTemp(si, goo, dong, type):  # 최고온도 출력은 type='MAX', 최저온도 출력은 type='MIN'
    # DB 불러오기
    conn = pymysql.connect(host='13.209.193.138', port=3306, user='root', passwd='test', db='mariaDB1', charset="utf8")
    try:
        cur = conn.cursor()
        sql = 'SELECT * FROM firstapp_xylocation'
        cur.execute(sql)
        result = cur.fetchall()
    finally:
        conn.close()

    df = pd.DataFrame(result, columns=["id", "si", "goo", "dong", "x", "y", "lon", "lat"])
    df1 = df.filter(items=['si', 'goo', 'dong', 'x', 'y', 'lon', 'lat'])  # (시, 구, 동, x, y) columns 필터링
    df2 = df1[df1['si'].isin([si]) & df1['goo'].isin([goo]) & df1['dong'].isin([dong])]
    nx = df2.iloc[0, 3]
    ny = df2.iloc[0, 4]

    vilage_weather_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst?"
    service_key = "nEOjm%2Bh6MajezPL97GQY7jDUzDS5L2qvhY4G%2BKfjjxqYULz7folcVjjKi1Q%2BgkD8P94Wowq7l24kNayBKGmsIA%3D%3D"

    today = datetime.datetime.today()  # 오늘의 날씨를 알려주는 함수
    current_date = today.strftime("%Y년%m월%d일")  # ex) 현재 날짜가 21년 5월 13일인 경우, '20210513' 출력
    current_time = today.strftime("%H%M")  # ex) 현재 시간이 14:15 인 경우, '1415' 출력
    tomorrow_date = today + datetime.timedelta(days=1)
    tomorrow_date = tomorrow_date.strftime("%Y%m%d")  # 내일 날짜
    base_time = '0200'  # 당일 02:00 발표시작으로 고정

    payload = "serviceKey=" + service_key + "&" + \
              "numOfRows=100" + "&" + \
              "pageNo=1" + "&" + \
              "dataType=json" + "&" + \
              "base_date=" + current_date + "&" + \
              "base_time=" + base_time + "&" + \
              "nx=" + str(nx) + "&" + \
              "ny=" + str(ny)

    # 값 요청
    res = requests.get(vilage_weather_url + payload)
    items = res.json().get('response').get('body').get('items')

    # 최고, 최저 온도
    for item in items['item']:
        if item['category'] == 'TMN':
            TMN = item['fcstValue']
        elif item['category'] == 'TMX':
            TMX = item['fcstValue']

    if type == 'MAX':
        return (TMX)
    elif type == 'MIN':
        return (TMN)



# 현재날씨 함수
def currentWeather(si, goo, dong):
    # DB 불러오기
    conn = pymysql.connect(host='13.209.193.138', port=3306, user='root', passwd='test', db='mariaDB1', charset="utf8")
    try:
        cur = conn.cursor()
        sql = 'SELECT * FROM firstapp_xylocation'
        cur.execute(sql)
        result = cur.fetchall()
    finally:
        conn.close()

    df = pd.DataFrame(result, columns=["id", "si", "goo", "dong", "x", "y", "lon", "lat"])
    df1 = df.filter(items=['si', 'goo', 'dong', 'x', 'y', 'lon', 'lat'])  # (시, 구, 동, x, y) columns 필터링
    df2 = df1[df1['si'].isin([si]) & df1['goo'].isin([goo]) & df1['dong'].isin([dong])]
    nx = df2.iloc[0, 3]
    ny = df2.iloc[0, 4]

    vilage_weather_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst?"
    service_key = "nEOjm%2Bh6MajezPL97GQY7jDUzDS5L2qvhY4G%2BKfjjxqYULz7folcVjjKi1Q%2BgkD8P94Wowq7l24kNayBKGmsIA%3D%3D"

    today = datetime.datetime.today()  # 오늘의 날씨를 알려주는 함수
    current_date = today.strftime("%Y년%m월%d일")  # ex) 현재 날짜가 21년 5월 13일인 경우, '20210513' 출력
    current_time = today.strftime("%H%M")  # ex) 현재 시간이 14:15 인 경우, '1415' 출력
    tomorrow_date = today + datetime.timedelta(days=1)
    tomorrow_date = tomorrow_date.strftime("%Y%m%d")  # 내일 날짜
    base_time = '0800'  # 당일 08:00 발표시작으로 고정

    payload = "serviceKey=" + service_key + "&" + \
              "numOfRows=100" + "&" + \
              "pageNo=1" + "&" + \
              "dataType=json" + "&" + \
              "base_date=" + current_date + "&" + \
              "base_time=" + base_time + "&" + \
              "nx=" + str(nx) + "&" + \
              "ny=" + str(ny)

    try:
        # 값 요청
        res = requests.get(vilage_weather_url + payload)
        items = res.json().get('response').get('body').get('items')

        for item in items['item']:
            if item['category'] == 'SKY':
                if item['fcstDate'] == current_date and '0000' < current_time <= '0300':
                    if item['fcstTime'] == '0300':
                        SKY = item['fcstValue']
                elif item['fcstDate'] == current_date and '0300' < current_time <= '0600':
                    if item['fcstTime'] == '0600':
                        SKY = item['fcstValue']
                elif item['fcstDate'] == current_date and '0600' < current_time <= '0900':
                    if item['fcstTime'] == '0900':
                        SKY = item['fcstValue']
                elif item['fcstDate'] == current_date and '0900' < current_time <= '1200':
                    if item['fcstTime'] == '1200':
                        SKY = item['fcstValue']
                elif item['fcstDate'] == current_date and '1200' < current_time <= '1500':
                    if item['fcstTime'] == '1500':
                        SKY = item['fcstValue']
                elif item['fcstDate'] == current_date and '1500' < current_time <= '1800':
                    if item['fcstTime'] == '1800':
                        SKY = item['fcstValue']
                elif item['fcstDate'] == current_date and '1800' < current_time <= '2100':
                    if item['fcstTime'] == '2100':
                        SKY = item['fcstValue']
                elif item['fcstDate'] == tomorrow_date and '2100' < current_time <= '0000':
                    if item['fcstTime'] == '0000':
                        SKY = item['fcstValue']
        if SKY == '1':
            result = '날씨는 맑습니다.'
        elif SKY == '3':
            result = '날씨는 구름이 많습니다.'
        elif SKY == '4':
            result = '날씨는 흐립니다.'
        else:
            result = '알수없음'
        # return (result)
    except:
        result = '날씨는 맑습니다.'

    tts=gTTS(text="오늘은 " + current_date + "입니다."  + result, lang='ko')
    tts.save('./test.wav')
    topic = "tts/message"

    #Die Variablen sind bei mir im Skript entsprechend angepasst 
    host = "13.209.193.138"
    port = 1883

    def on_message(client, obj, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    mqttc = mqtt.Client('python_pub')

    mqttc.on_message = on_message

    mqttc.connect(host, port)

    f = open('./test.wav', "rb")
    imagestring = f.read()
    f.close()
    byteArray = bytearray(imagestring)

    mqttc.publish(topic, byteArray)
    
    # rc = 0
    # while rc == 0:
    #     rc = mqttc.loop()
    print("test2")
    # os.remove('../message/today.wav')
    return ()

def my_job():
    #  Your job processing logic here... 
    # 
    # url = "http://127.0.0.1:8000/weatheralarm/"
    # return requests.get(url)
    print("test")
    currentWeather('서울특별시', '강서구', '가양제1동')
    


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            # trigger=CronTrigger(hour='17',minute="0"),  # 매일 아침 8시에 반복
            trigger=CronTrigger(second="*/10"),  # Every 10 seconds
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
            # scheduler.start()