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


    def reset_event_registration(self, user):
        try:
            inscription = Inscription.objects.get(user=user, event=self.event)
            inscription.delete()
        except Inscription.DoesNotExists:
            pass

    def create_event_registration(self, user):
        if not self.event:
            return
        print(Inscription.objects.update_or_create({
            'user': user,
            'event': self.event
        }, user=user, event=self.event))

    def update_event_registrations(self, old_event):
        """ Unsubscribe user from old event and subscribe them to the curretn one
        """
        if self.event != old_event:
            # Unsubscribe user from old event
            users = BuyingHistory.get_product_buyers(self)
            Inscription.objects.filter(user__in=users, event=old_event).delete()
            # subscribe user to new event
            with transaction.atomic():
                print(users)
                for user in users:
                    self.create_event_registration(user)

    def delete(self):
        users = BuyingHistory.get_product_buyers(self)
        Inscription.objects.filter(user__in=users, event=self.event).delete()
        super().delete()


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

    def update_event_registrations(self, old_events):
        current_products = self.products.filter(enabled=True).all()
        current_event = [p.event for p in current_products if p.event]

        removed_event = list(set(old_events) - set(current_event))
        for event in removed_event:
            users = BuyingHistory.get_pack_buyers(self)
            Inscription.objects.filter(user__in=users, event=event).delete()

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



