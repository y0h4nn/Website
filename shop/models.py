from collections import Counter
from django.contrib.auth.models import User
from django.db import models, IntegrityError, transaction
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
            print(users)
            for user in users:
                products = BuyingHistory.get_all_bought_products(user)
                print(products)
                event_products = [p for p in products if p.event == self.event]
                print(event_products)
                if len(event_products) <= 1:
                    Inscription.objects.filter(user=user, event=self.event).delete()


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
                product.create_event_registration(user)

    def update_event_registrations(self, old_products):
        current_products = self.products.filter(enabled=True).all()
        removed_products = list(set(old_products) - set(current_products))

        old_products_refs = Counter(old_products)
        current_products_refs = Counter(current_products)
        diff = {}
        for a in old_products_refs:
            for b in current_products_refs:
                if a == b:
                    diff[a] = old_products_refs[a] - current_products_refs[a]

        with transaction.atomic():
            users = BuyingHistory.get_pack_buyers(self)
            for product in removed_products:
                for user in users:
                    count = BuyingHistory.count_bought_products_of_kind(product, user)
                    if product in diff:
                        if count <= 0:
                            Inscription.objects.filter(user=user, event=product.event).delete()
                    elif product in old_products_refs:
                        if count <= 0:
                            Inscription.objects.filter(user=user, event=product.event).delete()

        with transaction.atomic():
            for product in current_products:
                users = BuyingHistory.get_product_buyers(product)
                for user in users:
                    product.create_event_registration(user)


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


    @staticmethod
    def get_product_buyers(product):
        packs = [p for p in Packs.objects.prefetch_related('products').all() if product in p.products.all()]
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
    def count_bought_products_of_kind(product, user):
        packs_entries = BuyingHistory.objects.filter(user=user,type='pack').all()
        products_entries = BuyingHistory.objects.filter(user=user, type='product').all()

        print(product.event)
        count = 0
        for item in packs_entries:
            print("pack %s " % str(item.pack))
            for p in item.pack.products.all():
                print(p.event)
                if product.event == p.event:
                    count += 1

        for item in products_entries:
            if product.event == item.product.event:
                count += 1

        print(count)
        return count
