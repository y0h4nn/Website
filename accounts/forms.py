from django.forms import ModelForm
from django.contrib.auth.models import User
from . import models

class UserForm(ModelForm):
    prefix = 'user'
    class Meta:
        model = User
        fields = ['last_name', 'first_name']

class ProfileForm(ModelForm):
    prefix = 'profile'

    class Meta:
        model = models.Profile
        fields = [
            'nickname',
            'picture',
            'birthdate',
            'family',
            'promo',
            'enib_join_year',
            'semester'
        ]
