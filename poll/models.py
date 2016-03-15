from django.utils import timezone
from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group
from bde.shortcuts import is_contributor


class Poll(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='polls')
    group = models.ForeignKey(Group, related_name='polls')
    title = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    contributor_only = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def is_open(self):
        return self.start_date <= timezone.now() <= self.end_date

    def is_ended(self):
        return timezone.now() >= self.end_date

    def can_vote(self, user):
        return user.is_authenticated() and (not self.contributor_only or is_contributor(user)) and self.group in user.groups.all()

    def can_see_results(self, user):
        return user.is_authenticated and self.group in user.groups.all()

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

