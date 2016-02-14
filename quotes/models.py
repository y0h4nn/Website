from django.db import models
from django.conf import settings
import random


class Prof(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Quote(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='quotes')
    prof = models.ForeignKey(Prof, related_name='quotes')
    text = models.TextField()
    approved = models.BooleanField(default=False)

    @classmethod
    def get_random(cls):
        count = cls.objects.filter(approved=True).count()
        if count:
            random_index = random.randint(0, count - 1)
            return cls.objects.filter(approved=True)[random_index]
        else:
            return None

    def __str__(self):
        return "{} - {}".format(self.text, self.prof.name)

