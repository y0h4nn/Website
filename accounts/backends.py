import requests
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import check_password
from django.db import IntegrityError


def normalize_username(username):
    return username[:30].replace('.', '_')


class BaseAuth:
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class NormalAuth(BaseAuth):
    def authenticate(self, email=None, password=None):
        if email and password:
            if '@' in email:
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    return None
            else:
                try:
                    user = User.objects.get(username=email)
                    print(user)
                except User.DoesNotExist:
                    return None
            if not check_password(password, user.password):
                return None
            return user



class CASAuth(BaseAuth):
    def authenticate(self, email=None, password=None):
        user = None
        if email and password:
            username = normalize_username(email.split("@")[0].strip())
            email = email.strip() + '@enib.fr' if '@' not in email else email
            r = requests.post('https://cas.enib.fr/v1/tickets/', data={'username': username, 'password': password})
            if r.status_code == 201:
                try:
                    user = User.objects.create_user(username, email, password)
                    enib_group = Group.objects.get(name='Enib')
                    enib_group.user_set.add(user)
                    user.save()
                except IntegrityError:
                    return None
        return user
