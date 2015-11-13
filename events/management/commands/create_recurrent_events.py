from django.core.management.base import BaseCommand, CommandError
from events.models import RecurrentEvent, Event
from django.utils import timezone
import datetime

class Command(BaseCommand):
    help = 'Create events based on reucrrent events.'

    def handle(self, *args, **options):
        for event in RecurrentEvent.objects.all():
            while True:
                if event.last_created is None or event.last_created < timezone.now() + datetime.timedelta(days=14):
                    self.update_event(event)
                else:
                    break
        self.stdout.write('Successfully created events')

    def update_event(self, event):
        delta = datetime.timedelta(days=event.delay)

        if event.last_created is None:  # First creation
            e = Event.objects.create(**{field: value for field, value in event.__dict__.items() if field in [field.column for field in Event._meta.fields if field.column not in ['id', 'model']]})
            e.save()
            event.last_created = e.start_time
            event.save()
            print("First creation of %s, start = %s (delay=%d)" % (event, event.start_time, event.delay))
        else:
            delta_dates = event.last_created - event.start_time + delta
            e = Event.objects.create(**{field: value for field, value in event.__dict__.items() if field in [field.column for field in Event._meta.fields if field.column not in ['id', 'model']]})
            e.start_time += delta_dates
            e.end_time += delta_dates
            e.end_inscriptions +=delta_dates
            if e.invitations_start is not None:
                e.invitations_start += delta_dates
            e.save()
            event.last_created = e.start_time
            event.save()
            print("Creating event %s for date %s" % (event, event.last_created))


