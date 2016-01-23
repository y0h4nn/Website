"""

Product and packs
=================


Warning this file is really easy to break and since there is not test yet so I
heavely discourage you from editing it.

Anyway if you must edit it be aware that whether event registration update are
done before or after product edition is not clear and may vary depending of the
item type. This implies that when checking if there is valid registration left
(another product bought by the user register for the same event) you must be
cautious to remove or not the deleted product from your count.

Good luck,
Arnaud

"""

from collections import Counter
from django.db import models, transaction
from django.conf import settings
from bde.models import Contributor
from events.models import Event, Inscription
from notifications.shortcuts import notify
import datetime


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
    event = models.ForeignKey(Event, null=True, blank=True, on_delete=models.SET_NULL, limit_choices_to={'start_time__gt': datetime.datetime.now()})
    description = models.TextField()
    enabled = models.BooleanField(default=True)

    class Meta:
        permissions = (
            ('sell_product', 'Can sell products'),
            ('manage_product', 'Can manage products and packs'),
        )

    def __str__(self):
        return self.name

    def buy(self, user, payment_mean, seller):
        buy = BuyingHistory(
            user=user,
            product=self,
            type='product',
            payment_mean=payment_mean,
            seller=seller,
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


    def create_event_registration(self, user):
        if not self.event:
            return
        Inscription.objects.update_or_create({
            'user': user,
            'event': self.event
        }, user=user, event=self.event)

    def update_event_registrations(self, old_event):
        """ Unsubscribe user from old event and subscribe them to the curretn one
        """
        if self.event != old_event:
            # Unsubscribe user from old event
            with transaction.atomic():
                users = BuyingHistory.get_product_buyers(self)
                for user in users:
                    products = BuyingHistory.get_all_bought_products(user)
                    event_products = [p for p in products if p.event == old_event]
                    if not len(event_products):
                        Inscription.objects.filter(user=user, event=old_event).delete()
                    self.create_event_registration(user)

    def reset_event_registrations(self):
        with transaction.atomic():
            users = BuyingHistory.get_product_buyers(self)
            for user in users:
                count = BuyingHistory.count_event_participations(self.event, user)
                print("%s; %s" % (user, count))
                if count <= 0:
                    Inscription.objects.filter(user=user, event=self.event).delete()


class Packs(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    products = models.ManyToManyField(Product, blank=True, limit_choices_to={'enabled': True})
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def buy(self, user, payment_mean, seller):
        buy = BuyingHistory(
            user=user,
            pack=self,
            type='pack',
            payment_mean=payment_mean,
            seller=seller
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
                product.create_event_registration(user)

    def update_event_registrations(self, old_products):
        current_products = self.products.filter(enabled=True).all()
        removed_products = list(set(old_products) - set(current_products))

        with transaction.atomic():
            users = BuyingHistory.get_pack_buyers(self)
            for product in removed_products:
                for user in users:
                    count = BuyingHistory.count_event_participations(product.event, user)
                    if count <= 0:
                        Inscription.objects.filter(user=user, event=product.event).delete()

        with transaction.atomic():
            for product in current_products:
                users = BuyingHistory.get_product_buyers(product)
                for user in users:
                    product.create_event_registration(user)

    def reset_event_registrations(self):
        with transaction.atomic():
            users = BuyingHistory.get_pack_buyers(self)
            events = []
            for product in self.products.filter(enabled=True).all():
                if product.event:
                    events.append(product.event)
            events_count = Counter(events)
            for event, count in events_count.items():
                for user in users:
                    event_participations = BuyingHistory.count_event_participations(event, user)
                    if count <= event_participations:
                        Inscription.objects.filter(user=user, event=event).delete()


TYPES = [
    ('product', 'Produit'),
    ('pack', 'Pack'),
]

class BuyingHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    type = models.CharField(max_length=10, choices=TYPES)
    product = models.ForeignKey(Product ,null=True, blank=True)
    pack = models.ForeignKey(Packs, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    payment_mean = models.CharField(max_length=10, choices=MEANS_OF_PAYMENT)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, default=None, related_name="seller")

    class Meta:
        permissions = (
            ('view_history', 'Can view history'),
        )

    def __str__(self):
        return "%s bought by %s" % (self.product or self.pack, self.user.profile)

    @staticmethod
    def get_product_buyers(product):
        packs = [p for p in Packs.objects.prefetch_related('products').filter(enabled=True).all() if product in p.products.filter(enabled=True).all()]
        users = [item.user for item in BuyingHistory.objects.filter(models.Q(product=product) | models.Q(pack__in=packs)).all()]
        return users

    @staticmethod
    def get_pack_buyers(pack):
        users = [item.user for item in BuyingHistory.objects.filter(pack=pack)]
        return users

    @staticmethod
    def get_all_bought_products(user):
        packs_entries = BuyingHistory.objects.filter(user=user,type='pack').all()
        products_entries = BuyingHistory.objects.filter(user=user, type='product').all()

        products = []
        for item in packs_entries:
            products += list(item.pack.products.filter(enabled=True).all())

        for item in products_entries:
            if item.product.enabled:
                products.append(item.product)

        return products

    @staticmethod
    def count_event_participations(event, user):
        """ Count event participation grandet buy user buying history.
        """
        packs_entries = BuyingHistory.objects.filter(user=user,type='pack').all()
        products_entries = BuyingHistory.objects.filter(user=user, type='product').all()

        count = 0
        for item in packs_entries:
            if not item.pack.enabled:
                continue
            for p in item.pack.products.filter(enabled=True).all():
                if event == p.event:
                    count += 1
        for item in products_entries:
            if event == item.product.event and item.product.enabled:
                count += 1
        return count

    def get_products(self):
        if self.type == 'pack':
            return self.pack.products.all()
        elif self.type == 'product':
            return [self.product]
