from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from .models import Contributor
from django.utils import timezone


def is_contributor(user):
    try:
        return user.contribution.end_date >= timezone.now().date()
    except Contributor.DoesNotExist as e:
        return False

