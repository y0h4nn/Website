from django.utils import timezone
from django.db import models
from django.conf import settings

class Poll(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='polls')
    title = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.title

    def is_open(self):
        return self.start_date <= timezone.now() <= self.end_date


class Question(models.Model):
    poll = models.ForeignKey('Poll', related_name='questions')
    text = models.TextField()

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey('Question', related_name='answers')
    text = models.TextField()
    votes = models.IntegerField()

    def __str__(self):
        return self.text


class Voter(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='voted_questions')
    poll = models.ForeignKey(Poll)

