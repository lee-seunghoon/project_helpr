from django.db import models

# Create your models here.


class Message(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(blank=True)
    # pub_at = models.DateTimeField(auto_now=True)


class Message2(models.Model):
    message = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    # pub_at = models.DateTimeField(auto_now=True)


