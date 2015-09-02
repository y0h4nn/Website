import imaplib
from django.contrib.auth.models import User, check_password, Group
from django.db import IntegrityError
from . import models


class BaseAuth:
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class NormalAuth(BaseAuth):
    def authenticate(self, email=None, password=None):
        if email and password:
            email = email + '@enib.fr' if '@' not in email else email
            try:
                user = User.objects.get(email=email)
                if not check_password(password, user.password):
                    return None
                return user
            except User.DoesNotExist:
                return None


class ImapAuth(BaseAuth):
    def authenticate(self, email=None, password=None):
        if email and password:
            # TODO use context manager when python 3.5 is out (sept 2015)
            # FIXME when python 3.5 is out
            srv = imaplib.IMAP4_SSL('imap-eleves.enib.fr')

            username = email.split("@")[0].strip()
            email = email.strip() + '@enib.fr' if '@' not in email else email
            user = None
            try:
                srv.login(username, password)
                user = User.objects.create_user(username, email, password)
                g1 = Group.objects.get(name='Enib')
                g2 = Group.objects.get(name='Tous')
                g1.user_set.add(user)
                g2.user_set.add(user)
                user.save()
            except (imaplib.IMAP4.error, IntegrityError):
                pass
            srv.logout()
            return user

