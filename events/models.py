from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q, Count, Sum
from django.templatetags.static import static
from django.utils import timezone
from django.utils.functional import cached_property
from bde.shortcuts import is_contributor
import uuid as u
import json


MEANS_OF_PAYMENT = [
    ('cash', 'Espèces'),
    ('check', 'Chèque'),
    ('card', 'Carte de crédit'),
]


class Event(models.Model):
    GESTION_WAF = "WAF"
    GESTION_NOLIMIT = "NL"
    GESTION_FORMULAS = "FOR"
    GESTION_CHOICES = [(None, 'Pas de gestion'),
                       (GESTION_WAF, 'Gestion style WAF'),
                       (GESTION_NOLIMIT, 'Gestion style no-limit'),
                       (GESTION_FORMULAS, 'Gestion formules'), ]

    name = models.CharField(max_length=255)
    end_inscriptions = models.DateTimeField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=19, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    photo = models.ImageField(null=True, blank=True)
    private = models.BooleanField(default=False)

    limited = models.BooleanField(default=False)
    max_inscriptions = models.IntegerField(validators=[MinValueValidator(0)], default=0)

    allow_extern = models.BooleanField(default=False)
    end_extern_inscriptions = models.DateTimeField(default=None, null=True, blank=True)

    allow_invitations = models.BooleanField(default=False)
    max_invitations = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    max_invitations_by_person = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    invitations_start = models.DateTimeField(null=True, blank=True)

    gestion = models.CharField(max_length=3, choices=GESTION_CHOICES, default=None, null=True, blank=True)
    photo_path = models.CharField(max_length=255, blank=True, default="")

    model = models.BooleanField(default=False)

    class Meta:
        permissions = (
            ('manage_entries', 'Can manage user entries'),
            ('manage_event', 'Can manage events (add/del/edit)'),
            ('access_list', 'Can view user list (needed for csv export)'),
        )

    def registrations_number(self):
        return self.inscriptions.all().count() + self.extern_inscriptions.all().count() + self.nb_invitations

    @cached_property
    def nb_invitations(self):
        return self.invitations.all().count()

    def nb_places_left(self):
        if self.limited:
            return self.max_inscriptions - self.registrations_number()

    def can_subscribe(self):
        return not self.limited or self.registrations_number() < self.max_inscriptions

    def can_invite(self, user):
        return (self.allow_invitations and
                (self.invitations_start is None or self.invitations_start <= timezone.now()) and
                ((self.max_invitations == 0 or (self.invitations.all().count() < self.max_invitations))and
                (self.max_invitations_by_person == 0 or self.invitations.filter(user=user).count() < self.max_invitations_by_person)) and
                is_contributor(user) and
                self.can_subscribe())

    def closed(self):
        return timezone.now() >= self.end_inscriptions

    def closed_extern(self):
        return self.closed() or (self.end_extern_inscriptions and timezone.now() >= self.end_extern_inscriptions)

    def photo_url(self):
        if self.photo:
            return self.photo.url
        return static('images/default_event_icon.png')

    def __str__(self):
        return self.name

    @staticmethod
    def to_come(user):
        events = [event for event in Event.objects.filter(
            Q(model=False),
            Q(end_inscriptions__gt=timezone.now()),
            Q(inscriptions__user=user) | Q(private=False)
        ).distinct().prefetch_related('formulas').order_by('start_time')\
        .annotate(reg_nb=(Count('inscriptions', distinct=True) + Count('extern_inscriptions', distinct=True) + Count('invitations', distinct=True)))\
        .extra(select={'ins': "(SELECT COUNT(*) FROM events_inscription WHERE events_inscription.event_id=events_event.id AND events_inscription.user_id=%d)" % user.id})]
        a = [(event.ins, event) for event in events]
        print(a)
        return a

    def formulas_json(self):
        res = {f.name: "{} <br>(Cotisant: {}€ / Non cotisant: {}€)".format(f.name, f.price_contributor, f.price_non_contributor) for f in self.formulas.all()}
        return json.dumps(res)


class RecurrentEvent(Event):
    delay = models.IntegerField(default=1)
    last_created = models.DateTimeField(null=True, blank=True, default=None)

    class Meta:
        permissions = (
            ('manage_recurrent_event', 'Can manage recurrent event (add/del/edit'),
        )


class ExternLink(models.Model):
    event = models.ForeignKey(Event, related_name="extern_links")
    uuid = models.UUIDField()
    admin_uuid = models.UUIDField(default=u.uuid4)
    maximum = models.IntegerField(validators=[MinValueValidator(1)])
    name = models.CharField(max_length=255)

    class Meta:
        unique_together = (('name', 'event'),)

    def places_left(self):
        return self.event.can_subscribe() and (self.nb_places_left() > 0)

    def nb_inscriptions(self):
        return self.inscriptions.all().count()

    def nb_places_left(self):
        if self.event.nb_places_left() is None:
            return self.maximum - self.nb_inscriptions()
        return min(self.event.nb_places_left(), self.maximum - self.nb_inscriptions())


class Formula(models.Model):
    name = models.CharField(max_length=255)
    event = models.ForeignKey(Event, related_name='formulas')
    price_contributor = models.IntegerField()
    price_non_contributor = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (('name', 'event'), )


class Inscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="inscriptions")
    event = models.ForeignKey(Event, related_name="inscriptions")
    formula = models.ForeignKey(Formula, related_name="inscriptions", null=True, blank=True)

    in_date = models.DateTimeField(null=True, blank=True, default=None)
    payment_mean = models.CharField(max_length=10, choices=MEANS_OF_PAYMENT, null=True, blank=True)

    class Meta:
        unique_together = (('user', 'event'),)


class ExternInscription(models.Model):
    mail = models.EmailField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    event = models.ForeignKey(Event, related_name="extern_inscriptions")
    formula = models.ForeignKey(Formula, related_name="extern_inscriptions", null=True, blank=True)

    via = models.ForeignKey(ExternLink, related_name="inscriptions")
    birth_date = models.DateField(null=True)

    in_date = models.DateTimeField(null=True, blank=True, default=None)
    payment_mean = models.CharField(max_length=10, choices=MEANS_OF_PAYMENT, null=True, blank=True)

    class Meta:
        unique_together = (('mail', 'event'),)


class Invitation(models.Model):
    mail = models.EmailField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    event = models.ForeignKey(Event, related_name="invitations")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="invitations")
    formula = models.ForeignKey(Formula, blank=True, null=True)

    in_date = models.DateTimeField(null=True, blank=True, default=None)
    payment_mean = models.CharField(max_length=10, choices=MEANS_OF_PAYMENT, null=True, blank=True)

    class Meta:
        unique_together = (('mail', 'event'), )

