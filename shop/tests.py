import datetime
import uuid
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from . import models
from events.models import Event, Inscription


class ModelsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('user', 'user@exemple.com', 'password')
        self.seller = User.objects.create_user('seller', 'seller@exemple.com', 'password')
        self.product = models.Product.objects.create(
            name='default',
            price=51.69,
            description='Default test product'
        )
        self.event = Event.objects.create(
            name='Test event',
            end_inscriptions=timezone.make_aware(datetime.datetime(3000, 5, 15, 15, 42)),
            start_time=timezone.make_aware(datetime.datetime(3000, 5, 15, 15, 43)),
            end_time=timezone.make_aware(datetime.datetime(3000, 5, 15, 15, 44)),
            location='Enib',
            description='Description',
        )

    def create_dummy_products(self, n=1):
        return [
            models.Product.objects.create(
                name=str(uuid.uuid4()),
                price=0,
                description="product",
            ) for i in range(n)
        ]

    def create_dummy_packs(self, pack_count=1, products_per_pack=5):
        packs = []
        for i in range(pack_count):
            products = self.create_dummy_products(products_per_pack)
            pack = models.Packs.objects.create(
                name=str(uuid.uuid4()),
                price=0,
                description="Pack",
            )
            pack.products = products
            pack.save()
            packs.append(pack)

        return packs

    def create_dummy_events(self, event_count=1):
        return [
            Event.objects.create(
                name=str(uuid.uuid4()),
                end_inscriptions=timezone.make_aware(datetime.datetime(3000, 5, 15, 15, 42)),
                start_time=timezone.make_aware(datetime.datetime(3000, 5, 15, 15, 43)),
                end_time=timezone.make_aware(datetime.datetime(3000, 5, 15, 15, 44)),
                location='Enib',
                description='Description',
            ) for i in range(event_count)
        ]

    def test_simple_buying(self):
        """ Testing simple product buying and payment means validity.
        """

        product_1 = models.Product.objects.create(
            name='product 1',
            price=0,
            description="Description",
        )

        buy_count = 0
        for mean in models.MEANS_OF_PAYMENT:
            product_1.buy(self.user, mean[0], self.seller)
            buy_count += 1
            history_count = models.BuyingHistory.objects.filter(
                product=product_1,
                user=self.user,
            ).count()
            self.assertEqual(history_count, buy_count)

    def test_event_auto_registration_with_product(self):
        self.assertEqual(Inscription.objects.filter(event=self.event, user=self.user).count(), 0)
        product_event = models.Product.objects.create(
            name='Product event',
            price=0,
            description='Description',
            event=self.event,
        )
        product_event.buy(self.user, models.MEANS_OF_PAYMENT[0][0], self.seller)
        self.assertEqual(Inscription.objects.filter(event=self.event, user=self.user).count(), 1)

    def test_event_auto_registration_with_pack(self):
        events = self.create_dummy_events(2)
        pack = self.create_dummy_packs(1, 2)[0]

        first = pack.products.first()
        first.event = events[0]
        first.save()

        last = pack.products.last()
        last.event = events[1]
        last.save()

        pack.buy(self.user, models.MEANS_OF_PAYMENT[0][0], self.seller)

        self.assertEqual(Inscription.objects.filter(event=events[0], user=self.user).count(), 1)
        self.assertEqual(Inscription.objects.filter(event=events[1], user=self.user).count(), 1)




