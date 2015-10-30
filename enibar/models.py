from django.db import models


class Note(models.Model):
    foreign_id = models.IntegerField(unique=True)
    nickname = models.CharField(max_length=255)
    mail = models.EmailField()
    note = models.DecimalField(max_digits=10, decimal_places=2)


class Category(models.Model):
    foreign_id = models.IntegerField()
    name = models.CharField(max_length=255)
    alcoholic = models.BooleanField()


class PriceDescription(models.Model):
    foreign_id = models.IntegerField()
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category)


class Product(models.Model):
    foreign_id = models.IntegerField()
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category)


class Price(models.Model):
    foreign_id = models.IntegerField()
    description = models.ForeignKey(PriceDescription)
    product = models.ForeignKey(Product)
    value = models.DecimalField(max_digits=10, decimal_places=2)


class HistoryLine(models.Model):
    foreign_id = models.IntegerField()
    note = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    product = models.CharField(max_length=255)
    price_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

