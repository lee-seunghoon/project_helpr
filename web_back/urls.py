from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

urlpatterns = [
    path('insert/', views.region_code, name='insert'),  # xyLocation update url
    # path('주소/', 명령(일반적으로 함수를 불러온다), name="인덱스"),
    # path('', views.chart, name='chart'),
    path('chart/', views.chart, name='chart'),
    path('map/', views.map, name='map'),
    path('msg/', views.msg, name='msg'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
]