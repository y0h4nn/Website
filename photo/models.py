from django.db import models
from django.contrib.auth.models import User, Group
from events.models import Inscription, Event, ExternInscription, Invitation

class StandaloneAppPermissions(models.Model):
    class Meta:
        permissions = (
            ('manage_access_policy', 'Can manage access policies'),
        )

class AccessPolicy(models.Model):
    path = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def get_class_name(self):
        """ Because I need to access __name__ from template
        """
        return self.__class__.__name__

    @staticmethod
    def list(path):
        """ Get the list of all database objects which are subclasses of
        AccessPolicy for given path.
        """
        access_list = []
        for cls in AccessPolicy.__subclasses__():
            access_list.extend(cls.objects.filter(path=path).all())
        return access_list

    def user_can_access(self, user):
        raise NotImplementedError


    def extern_can_access(self, email):
        raise NotImplementedError


class PublicAccess(AccessPolicy):
    class Meta:
        unique_together = ('path',)

    def user_can_access(self, user):
        return True

    def extern_can_access(self, email):
        return True

    def __str__(self):
        return "Tous le monde peut voir l'album"


class GroupAccess(AccessPolicy):
    group = models.ForeignKey(Group)

    class Meta:
        unique_together = ('path', 'group')

    def user_can_access(self, user):
        if not user:
            return False
        if self.group in user.groups.all():
            return True
        return False

    def extern_can_access(self, email):
        return False

    def __str__(self):
        return "Le groupe %s peut voir l'album" % self.group.name


class EventAccess(AccessPolicy):
    event = models.ForeignKey(Event)

    class Meta:
        unique_together = ('path', 'event')

    def user_can_access(self, user):
        if not user:
            return False
        try:
            inscription = Inscription.objects.get(user=user, event=self.event)
            return bool(inscription.in_date)
        except Inscription.DoesNotExist:
            return False

    def extern_can_access(self, email):
        can_access = False
        try:
            inscription = ExternInscription.objects.get(mail=email, event=self.event)
            can_access |= bool(inscription.in_date)
        except ExternInscription.DoesNotExist:
            pass

        try:
            invitation = Invitation.objects.get(mail=email, event=self.event)
            can_access |= bool(invitation.in_date)
        except Invitation.DoesNotExist:
            pass

        return can_access

    def __str__(self):
        return "Les participants de l'évènement %s peuvent voir l'album" % self.event.name


def get_models():
    return {c.__name__: c for c in AccessPolicy.__subclasses__()}
