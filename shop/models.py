from django.contrib.auth.models import User
from django.db import models, IntegrityError
from django.conf import settings
from bde.models import Contributor
from events.models import Event, Inscription
from notifications import notify


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
    event = models.ForeignKey(Event, null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField()
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def buy(self, user, payment_mean):
        buy = BuyingHistory(
            user=user,
            product=self,
            type='product',
            payment_mean=payment_mean
        )
        buy.save()
        notify(
            "Confirmation de l'achat de «%s»" % self.name,
            "shop:index", {},
            users=[user]
        )
        fnc = ACTIONS_FNC_MAPPING[self.action]
        fnc(user, self, payment_mean)

        if self.event:
            self.create_event_registration(user)


    def reset_event_registration(self, user):
        try:
            inscription = Inscription.objects.get(user=user, event=self.event)
            inscription.delete()
        except Inscription.DoesNotExists:
            pass

    def create_event_registration(self, user):
        try:
            Inscription.objects.create(user=user, event=self.event)
        except IntegrityError:
            pass


class Packs(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    products = models.ManyToManyField(Product, blank=True, limit_choices_to={'enabled': True})
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def buy(self, user, payment_mean):
        buy = BuyingHistory(
            user=user,
            pack=self,
            type='pack',
            payment_mean=payment_mean
        )
        buy.save()
        notify(
            "Confirmation de l'achat de «%s»" % self.name,
            "shop:index", {},
            users=[user]
        )

        for product in self.products.filter(enabled=True).all():
            fnc = ACTIONS_FNC_MAPPING[product.action]
            fnc(user, product, payment_mean)
            if product.event:
                try:
                    Inscription.objects.create(user=user, event=product.event)
                except IntegrityError:
                    pass

TYPES = [
    ('product', 'Produit'),
    ('pack', 'Pack'),
]

class BuyingHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    type = models.CharField(max_length=10, choices=TYPES)
    product = models.ForeignKey(Product ,null=True, default=None)
    pack = models.ForeignKey(Packs, null=True, default=None)
    date = models.DateTimeField(auto_now_add=True)
    payment_mean = models.CharField(max_length=10, choices=MEANS_OF_PAYMENT)


