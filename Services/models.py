from django.db import models
from blog.models import Article


class Comment(models.Model):
    messageContent = models.CharField(max_length=2000, blank=True, default='')
    created = models.DateTimeField(auto_now_add=True)
    userName = models.CharField(max_length=100, blank=True, default='')
    userContact = models.CharField(max_length=200, blank=True, default='')
    userIp = models.CharField(max_length=20, blank=True, default='')
    isValid = models.BooleanField(default=True)
    article_id = models.IntegerField(max_length=5, blank=True)

    class Meta:
        ordering = ('created',)


class Evaluation(models.Model):
    viewCount = models.IntegerField(max_length=10, blank=True, default=0)
    praiseCount = models.IntegerField(max_length=10, blank=True, default=0)
    article_id = models.IntegerField(max_length=5, blank=True)


class Announcement(models.Model):
    announcement = models.CharField(max_length=1000, blank=True, default='')
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()