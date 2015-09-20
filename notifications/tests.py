import uuid
from django.test import TestCase
from django.contrib.auth.models import User, Group
from . import notify
from . import models

class TestNotifications(TestCase):


    def test_group_notifications(self):
        group = Group.objects.create(name=str(uuid.uuid4()))
        user_count = 10
        for i in range(user_count):
            user = User.objects.create_user(
                    str(uuid.uuid4())[:30],
                'user@exemple.com',
                'password'
            )
            user.groups.add(group)
            user.save()

        notify(
            'notification message',
            'notifications:index',
            groups=[group]
        )


        self.assertEqual(models.Notification.objects.all().count(), user_count)

    def test_user_notification(self):
        user = User.objects.create_user(
            str(uuid.uuid4())[:30],
            'user@exemple.com',
            'password'
        )
        notify(
            'notification message',
            'notifications:index',
            users=[user]
        )
        self.assertEqual(models.Notification.objects.all().count(), 1)
