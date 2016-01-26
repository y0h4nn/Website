import uuid
import datetime
from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.utils import timezone
from events import models as event_models
from . import models
from . import views

class AccessTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('user', 'user@example.com', 'password')
        self.group = Group.objects.create(name="AccessGroup")


    def test_public_access(self):
        models.PublicAccess.objects.create(path="/public")

        self.assertTrue(views.can_access("/public"))
        self.assertTrue(views.can_access("/public", self.user))
        self.assertTrue(views.can_access("/public", email="extern@example.com"))


    def test_group_access(self):
        models.GroupAccess.objects.create(path="/groups", group=self.group)

        self.assertFalse(views.can_access("/groups"))
        self.assertFalse(views.can_access("/groups", self.user))
        self.assertFalse(views.can_access("/groups", email="extern@example.com"))

        self.group.user_set.add(self.user)

        self.assertTrue(views.can_access("/groups", self.user))

    def test_event_access(self):
        event = event_models.Event.objects.create(
            name='Test event',
            end_inscriptions=timezone.make_aware(datetime.datetime(3000, 5, 15, 15, 42)),
            start_time=timezone.make_aware(datetime.datetime(3000, 5, 15, 15, 43)),
            end_time=timezone.make_aware(datetime.datetime(3000, 5, 15, 15, 44)),
            location='Enib',
            description='Description',
        )

        models.EventAccess.objects.create(path="/event", event=event)

        self.assertFalse(views.can_access("/event"))
        self.assertFalse(views.can_access("/event", self.user))
        self.assertFalse(views.can_access("/event", email="extern@example.com"))

        inscription = event_models.Inscription.objects.create(user=self.user, event=event)
        self.assertFalse(views.can_access("/event", self.user))
        inscription.in_date = timezone.now()
        inscription.save()
        self.assertTrue(views.can_access("/event", self.user))

        link = event_models.ExternLink.objects.create(
            event=event,
            maximum=10,
            name="Extern inscription",
            uuid=str(uuid.uuid4())
        )
        ext_inscription = event_models.ExternInscription.objects.create(
            mail='extern@example.com',
            first_name='Extern',
            last_name='Extern',
            event=event,
            via=link
        )

        self.assertFalse(views.can_access("/event", email='extern@example.com'))
        ext_inscription.in_date = timezone.now()
        ext_inscription.save()
        self.assertTrue(views.can_access("/event", email="extern@example.com"))


        invitation = event_models.Invitation(
            mail='invited@example.com',
            first_name='Invited',
            last_name='Invited',
            birth_date=timezone.now(),
            event=event,
            user=self.user
        )

        self.assertFalse(views.can_access("/event", email="invited@example.com"))
        invitation.in_date = timezone.now()
        invitation.save()
        self.assertTrue(views.can_access("/event", email="invited@example.com"))
