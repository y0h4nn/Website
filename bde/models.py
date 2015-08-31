import datetime
from django.db import models
from django.conf import settings

CONTRIBUTION_TYPES = [
    ('half', 'Demi-cotisation'),
    ('full', 'Cotisation'),
]

MEANS_OF_PAYMENT = [
    ('cash', 'Espèces'),
    ('check', 'Chèque'),
    ('card', 'Carte'),
]

class Contributor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="contribution")
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    type = models.CharField(max_length=4, choices=CONTRIBUTION_TYPES)
    means_of_payment = models.CharField(max_length=5, choices=MEANS_OF_PAYMENT)

    @staticmethod
    def take_half_contribution(user, mean):
        now = datetime.datetime.now()
        if 1 <= now.month <= 6:
            endate = datetime.date(now.year, 6, 30)
        else:
            endate = datetime.date(now.year, 12, 31)

        return Contributor.objects.update_or_create({
            'end_date': endate,
            'type': 'half',
            'means_of_payment': mean,
        }, user=user)

    @staticmethod
    def take_full_contribution(user, mean):
        now = datetime.datetime.now()
        if 8 <= now.month <= 12:
            endate = datetime.date(now.year + 1, 6, 30)
        else:
            return None

        return Contributor.objects.update_or_create({
            'end_date': endate,
            'type': 'full',
            'means_of_payment': mean,
        }, user=user)

