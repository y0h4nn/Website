from django.db import models
from django.conf import settings
from bde.models import Contributor


ACTIONS = [
    (None, 'Ne rien faire'),
    ('fullcontribution', 'Attribuer une contisation complete'),
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
    price = models.PositiveIntegerField()
    action = models.CharField(max_length=100, choices=ACTIONS, null=True, blank=True)

    def __str__(self):
        return self.name


class BuyingHistory(models.Model):
    username = models.CharField(max_length=80)
    product = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    payment_mean = models.CharField(max_length=10, choices=MEANS_OF_PAYMENT)
