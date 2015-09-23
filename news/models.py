from django.db import models
from django.conf import settings


class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)

class Comment(models.Model):
    news = models.ForeignKey(News, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

