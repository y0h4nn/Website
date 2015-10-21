from django import forms
from . import models


class AccessPolicyForm(forms.ModelForm):
    class Meta:
        model = models.AccessPolicy
        exclude = ['path']


class PublicAccessForm(AccessPolicyForm):
    class Meta:
        model = models.PublicAccess
        exclude = ['path']

class GroupAccessForm(AccessPolicyForm):
    class Meta:
        model = models.GroupAccess
        fields = ['group']


class EventAccessForm(AccessPolicyForm):
    class Meta:
        model = models.EventAccess
        fields = ['event']


POLICIES_FORMS = {
    'public': PublicAccessForm,
    'group': GroupAccessForm,
    'event': EventAccessForm,
}
