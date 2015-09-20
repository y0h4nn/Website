from freezegun import freeze_time
from django.test import TestCase
from .models import Event, Inscription, ExternInscription, ExternLink
from django.contrib.auth.models import User
import datetime
import uuid
from datetime import timezone
from django.templatetags.static import static


class TestEvent(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            name="test",
            end_inscriptions=datetime.datetime(2014, 7, 14, 12, 0, 0, tzinfo=timezone.utc),
            start_time=datetime.datetime(2014, 7, 14, 13, 0, 0, tzinfo=timezone.utc),
            end_time=datetime.datetime(2014, 7, 14, 14, 0, 0, tzinfo=timezone.utc),
            location="location",
            description="description",
            price=0,
            photo="",
            private=False,
            limited=False,
            max_inscriptions=0,
            allow_extern=False
        )

    def do_inscriptions(self, event, nb, extern=False):
        users = []
        if extern:
            ext = ExternLink.objects.create(event=event,
                uuid=uuid.uuid4(),
                maximum=10,
                name=uuid.uuid4()
            )

        for i in range(nb):
            if extern:
                ExternInscription.objects.create(mail='{}@lol.com'.format(uuid.uuid4()),
                    first_name="f",
                    last_name="l",
                    event=event,
                    via=ext
                )
            else:
                u = User.objects.create_user(str(uuid.uuid4())[:30], 'AAA{}@exemple.com'.format(i), 'AAA')
                Inscription.objects.create(user=u, event=event)

        return users


    def test_closed(self):
        with freeze_time("2014-07-14 11:00:00"):
            self.assertFalse(self.event.closed())
        with freeze_time("2014-07-14 11:59:59"):
            self.assertFalse(self.event.closed())
        with freeze_time("2014-07-14 12:00:00"):
            self.assertTrue(self.event.closed())

    def test_photo_url(self):
        self.assertEqual(self.event.photo_url(), static('images/default_event_icon.png'))
        self.event.photo = "coucou.png"
        self.event.save()
        self.assertEqual(self.event.photo_url(), '/static/medias/coucou.png')

    def test_can_subscribe(self):
        self.assertTrue(self.event.can_subscribe())
        self.event.limited = True
        self.event.max_inscriptions = 5
        self.event.save()
        self.do_inscriptions(self.event, 3)
        self.assertTrue(self.event.can_subscribe())
        self.do_inscriptions(self.event, 1)
        self.assertTrue(self.event.can_subscribe())
        self.do_inscriptions(self.event, 1)
        self.assertFalse(self.event.can_subscribe())

    def test_registrations_number(self):
        self.do_inscriptions(self.event, 4)
        self.do_inscriptions(self.event, 4, True)
        self.do_inscriptions(self.event, 5, True)
        self.assertEqual(self.event.registrations_number(), 13)

    def test_externam_link(self):
        ext = ExternLink.objects.create(event=self.event,
            uuid=uuid.uuid4(),
            maximum=10,
            name=uuid.uuid4()
        )
        for i in range(5):
            ExternInscription.objects.create(mail='{}@lol.com'.format(uuid.uuid4()),
                first_name="f",
                last_name="l",
                event=self.event,
                via=ext
            )
        self.assertTrue(ext.places_left())

        for i in range(5):
            ExternInscription.objects.create(mail='{}@lol.com'.format(uuid.uuid4()),
                first_name="f",
                last_name="l",
                event=self.event,
                via=ext
            )
        self.assertFalse(ext.places_left())

    @freeze_time("2014-07-14 11:00:00")
    def test_to_come(self):
        # Event open
        e1 = Event.objects.create(name="test", end_inscriptions=datetime.datetime(2014, 7, 14, 12, 0, 0, tzinfo=timezone.utc), start_time=datetime.datetime(2014, 7, 14, 13, 0, 0, tzinfo=timezone.utc), end_time=datetime.datetime(2014, 7, 14, 14, 0, 0, tzinfo=timezone.utc), location="location", description="description", price=0, photo="", private=False, limited=False, max_inscriptions=0, allow_extern=False)
        # Private event
        e2 = Event.objects.create(name="test2", end_inscriptions=datetime.datetime(2014, 7, 14, 12, 0, 0, tzinfo=timezone.utc), start_time=datetime.datetime(2014, 7, 14, 13, 0, 0, tzinfo=timezone.utc), end_time=datetime.datetime(2014, 7, 14, 14, 0, 0, tzinfo=timezone.utc), location="location", description="description", price=0, photo="", private=True, limited=False, max_inscriptions=0, allow_extern=False)
        # Closed private event
        e3 = Event.objects.create(name="test3", end_inscriptions=datetime.datetime(2014, 7, 13, 12, 0, 0, tzinfo=timezone.utc), start_time=datetime.datetime(2014, 7, 13, 13, 0, 0, tzinfo=timezone.utc), end_time=datetime.datetime(2014, 7, 13, 14, 0, 0, tzinfo=timezone.utc), location="location", description="description", price=0, photo="", private=True, limited=False, max_inscriptions=0, allow_extern=False)
        # Closed event
        e4 = Event.objects.create(name="test4", end_inscriptions=datetime.datetime(2014, 7, 13, 12, 0, 0, tzinfo=timezone.utc), start_time=datetime.datetime(2014, 7, 13, 13, 0, 0, tzinfo=timezone.utc), end_time=datetime.datetime(2014, 7, 13, 14, 0, 0, tzinfo=timezone.utc), location="location", description="description", price=0, photo="", private=False, limited=False, max_inscriptions=0, allow_extern=False)

        u = User.objects.create_user(str(uuid.uuid4())[:30], 'BBB@exemple.com', 'AAA')
        Inscription.objects.create(user=u, event=e2)
        u2 = User.objects.create_user(str(uuid.uuid4())[:30], 'CCC@exemple.com', 'AAA')

        self.assertEqual(Event.to_come(u), [(0, self.event), (0, e1), (1, e2)])
        self.assertEqual(Event.to_come(u2), [(0, self.event), (0, e1)])

