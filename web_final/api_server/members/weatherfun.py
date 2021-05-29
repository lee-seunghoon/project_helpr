import pymysql
import datetime
import pandas as pd
import requests

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
    current_date = today.strftime("%Y%m%d")  # ex) 현재 날짜가 21년 5월 13일인 경우, '20210513' 출력
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


# 현재온도 함수
def currentTemp(si, goo, dong):
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
    current_date = today.strftime("%Y%m%d")  # ex) 현재 날짜가 21년 5월 13일인 경우, '20210513' 출력
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
            if item['category'] == 'T3H':
                if item['fcstDate'] == current_date and '0000' < current_time <= '0300':
                    if item['fcstTime'] == '0300':
                        T3H = item['fcstValue']
                elif item['fcstDate'] == current_date and '0300' < current_time <= '0600':
                    if item['fcstTime'] == '0600':
                        T3H = item['fcstValue']
                elif item['fcstDate'] == current_date and '0600' < current_time <= '0900':
                    if item['fcstTime'] == '0900':
                        T3H = item['fcstValue']
                elif item['fcstDate'] == current_date and '0900' < current_time <= '1200':
                    if item['fcstTime'] == '1200':
                        T3H = item['fcstValue']
                elif item['fcstDate'] == current_date and '1200' < current_time <= '1500':
                    if item['fcstTime'] == '1500':
                        T3H = item['fcstValue']
                elif item['fcstDate'] == current_date and '1500' < current_time <= '1800':
                    if item['fcstTime'] == '1800':
                        T3H = item['fcstValue']
                elif item['fcstDate'] == current_date and '1800' < current_time <= '2100':
                    if item['fcstTime'] == '2100':
                        T3H = item['fcstValue']
                elif item['fcstDate'] == tomorrow_date and '2100' < current_time <= '0000':
                    if item['fcstTime'] == '0000':
                        T3H = item['fcstValue']
        return (T3H)
    except:
        T3H = '점검중'
        return (T3H)


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
    current_date = today.strftime("%Y%m%d")  # ex) 현재 날짜가 21년 5월 13일인 경우, '20210513' 출력
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
            result = '맑음'
        elif SKY == '3':
            result = '구름많음'
        elif SKY == '4':
            result = '흐림'
        else:
            result = '알수없음'
        return (result)
    except:
        result = '점검중'
        return (result)