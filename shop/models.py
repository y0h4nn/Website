from django.db import models
from django.conf import settings
from bde.models import Contributor


ACTIONS = [
    (None, 'Ne rien faire'),
    ('fullcontribution', 'Attribuer une cotisation complete'),
    ('halfcontribution', 'Attribuer une demi cotisation'),
]


ACTIONS_FNC_MAPPING = {
    None: lambda u, p, m: None,
    'fullcontribution': lambda u, p, m: Contributor.take_full_contribution(u, m),
    'halfcontribution': lambda u, p, m: Contributor.take_half_contribution(u, m),
}

MEANS_OF_PAYMENT = [
    ('cash', 'Espèces'),
    ('check', 'Chèque'),
    ('card', 'Carte de crédit'),
]


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    action = models.CharField(max_length=100, choices=ACTIONS, null=True, blank=True)
    description = models.TextField()
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Packs(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    products = models.ManyToManyField(Product, blank=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name


TYPES = [
    ('product', 'Produit'),
    ('pack', 'Pack'),
]

class BuyingHistory(models.Model):
    username = models.CharField(max_length=80)
    type = models.CharField(max_length=10, choices=TYPES)
    product = models.ForeignKey(Product ,null=True, default=None)
    pack = models.ForeignKey(Packs, null=True, default=None)
    date = models.DateTimeField(auto_now_add=True)
    payment_mean = models.CharField(max_length=10, choices=MEANS_OF_PAYMENT)


