from django.urls import path
from . import views

urlpatterns = [
    # path('주소/', 명령(일반적으로 함수를 불러온다), name="인덱스"),
    path('', views.chart, name='chart'),
    path('chart/', views.chart, name='chart'),
    path('map/', views.map, name='map'),
    path('msg/', views.msg, name='msg'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
]