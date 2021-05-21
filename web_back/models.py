from django.db import models

# Create your models here.
# 회원db
class User(models.Model):
    user_id = models.CharField(max_length=128, primary_key=True)
    user_pw = models.CharField(max_length=128)
    user_email= models.CharField(max_length=128)
    region_1 = models.CharField(max_length=128)
    region_2 = models.CharField(max_length=128)
    region_3 = models.CharField(max_length=128)
    region_x = models.IntegerField()
    region_y = models.IntegerField()


# region_1,2,3으로 지역
class xyLocation(models.Model):
    region_code = models.CharField(max_length=128, primary_key=True)
    region_1 = models.CharField(max_length=128)
    region_2 = models.CharField(max_length=128, null=True)
    region_3 = models.CharField(max_length=128, null=True)
    region_x = models.IntegerField()
    region_y = models.IntegerField()


class Message(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    content = models.TextField()



class chatData(models.Model):
    Q = models.CharField(max_length=128)
    A = models.CharField(max_length=128)