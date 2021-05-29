from .models import User, xyLocation, Message
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields  = ('user_id', 'user_pw', 'region_1', 
                    'region_2', 'region_3', 'retion_x', 'region_y')


class xyLocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = xyLocation
        fields  = ('region_code', 'region_1', 'region_2', 'region_3', 
                   'retion_x', 'region_y')


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields  = ( 'user_id', 'content')