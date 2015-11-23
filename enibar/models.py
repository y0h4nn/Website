from django.db import models


class Note(models.Model):
    foreign_id = models.IntegerField(unique=True)
    nickname = models.CharField(max_length=255)
    mail = models.EmailField()
    note = models.DecimalField(max_digits=10, decimal_places=2)


class HistoryLine(models.Model):
    foreign_id = models.IntegerField()
    note = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    product = models.CharField(max_length=255)
    price_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

