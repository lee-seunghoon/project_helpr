from django.db import models

# Create your models here.
class chatQdata(models.Model):
    id = models.IntegerField(primary_key=True)
    question = models.CharField(max_length=128)

class totalStopwords(models.Model):
    id = models.IntegerField(primary_key=True)
    stopword = models.CharField(max_length=128)


class senior_sentiment_dictionary(models.Model):
    id = models.IntegerField(primary_key=True)
    word = models.CharField(max_length=100)
    polarity = models.IntegerField()
    sentiment = models.CharField(max_length=10)
