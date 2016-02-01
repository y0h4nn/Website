from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
import os
import json
from events.models import Event


class TestEventAPI(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username="Test",
            password="test",
            email="test@exemple.com"
        )
        self.user2 = User.objects.create(
            username="Test2",
            password="test",
            email="test@exemple.com"
        )

    def create_dummy_event(self, name, end_inscription, start_time, end_time, **kwargs):
        event = Event.objects.create(
            name=name,
            end_inscriptions=end_inscription,
            start_time=start_time,
            end_time=end_time,
            location="Location",
            description="Description",
            **kwargs
        )
        return event

    def get(self, url):
        return self.client.get(url).json()

    def post(self, url, data):
        return json.loads(self.client.post(url, json.dumps(data), content_type="application/json").content.decode())

    def test_subscription(self):
        event = self.create_dummy_event(
            "Test event",
            timezone.now() + datetime.timedelta(days=1),
            timezone.now() + datetime.timedelta(days=2),
            timezone.now() + datetime.timedelta(days=3)
        )

        self.client.force_login(self.user)
        json_resp = self.get('/api/events/')
        self.assertEqual(event.name, json_resp[0]['name'])
        json_resp = self.get('/api/events/%s/get_registration/' % event.pk)
        self.assertFalse(json_resp['user_is_registered'])

        # register
        json_resp = self.post('/api/events/%s/set_registration/' % event.pk, {
            'registration': True,
        })
        self.assertTrue(json_resp['user_is_registered'])
        json_resp = self.get('/api/events/%s/get_registration/' % event.pk)
        self.assertTrue(json_resp['user_is_registered'])

        json_resp = self.post('/api/events/%s/set_registration/' % event.pk, {
            'registration': False,
        })
        self.assertFalse(json_resp['user_is_registered'])
        json_resp = self.get('/api/events/%s/get_registration/' % event.pk)
        self.assertFalse(json_resp['user_is_registered'])

    def test_closed_event_subscription(self):
        event = self.create_dummy_event(
            "Test event",
            timezone.now() - datetime.timedelta(days=4),
            timezone.now() - datetime.timedelta(days=3),
            timezone.now() - datetime.timedelta(days=2)
        )

        self.client.force_login(self.user)
        json_resp = self.get('/api/events/')
        self.assertEqual(event.name, json_resp[0]['name'])
        json_resp = self.get('/api/events/%s/get_registration/' % event.pk)
        self.assertFalse(json_resp['user_is_registered'])

        json_resp = self.post('/api/events/%s/set_registration/' % event.pk, {
            'registration': True,
        })
        json_resp = self.get('/api/events/%s/get_registration/' % event.pk)
        self.assertFalse(json_resp['user_is_registered'])

    def test_private_subscription(self):
        event = self.create_dummy_event(
            "Test event",
            timezone.now() + datetime.timedelta(days=1),
            timezone.now() + datetime.timedelta(days=2),
            timezone.now() + datetime.timedelta(days=3),
            private=True
        )
        self.client.force_login(self.user)
        json_resp = self.get('/api/events/')
        self.assertEqual(0, len(json_resp))

    def test_full_registration(self):
        event = self.create_dummy_event(
            "Test event",
            timezone.now() + datetime.timedelta(days=1),
            timezone.now() + datetime.timedelta(days=2),
            timezone.now() + datetime.timedelta(days=3),
            limited=True,
            max_inscriptions=1
        )
        self.client.force_login(self.user)
        json_resp = self.post('/api/events/%s/set_registration/' % event.pk, {
            'registration': True,
        })
        self.client.logout()
        self.client.force_login(self.user2)
        json_resp = self.post('/api/events/%s/set_registration/' % event.pk, {
            'registration': True,
        })
        json_resp = self.get('/api/events/%s/get_registration/' % event.pk)
        self.assertFalse(json_resp['user_is_registered'])

    def test_multiple_registration(self):
        event = self.create_dummy_event(
            "Test event",
            timezone.now() + datetime.timedelta(days=1),
            timezone.now() + datetime.timedelta(days=2),
            timezone.now() + datetime.timedelta(days=3),
        )
        self.client.force_login(self.user)
        json_resp = self.post('/api/events/%s/set_registration/' % event.pk, {
            'registration': True,
        })
        self.assertTrue(json_resp['user_is_registered'])
        json_resp = self.post('/api/events/%s/set_registration/' % event.pk, {
            'registration': True,
        })
        self.assertTrue(json_resp['user_is_registered'])

    def test_invalid_removal(self):
        event = self.create_dummy_event(
            "Test event",
            timezone.now() + datetime.timedelta(days=1),
            timezone.now() + datetime.timedelta(days=2),
            timezone.now() + datetime.timedelta(days=3),
        )
        self.client.force_login(self.user)
        json_resp = self.post('/api/events/%s/set_registration/' % event.pk, {
            'registration': False,
        })
        self.assertFalse(json_resp['user_is_registered'])

