from django.db import models
from django.contrib.auth.models import User, Group
from events.models import Inscription, Event



class AccessPolicy(models.Model):
    path = models.CharField(max_length=255)

    class Meta:
        abstract = True

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


class PublicAccess(AccessPolicy):
    class Meta:
        unique_together = ('path',)

    def user_can_access(self, user):
        return True

    def __str__(self):
        return "Tous le monde peut voir l'album"


class GroupAccess(AccessPolicy):
    group = models.ForeignKey(Group)

    class Meta:
        unique_together = ('path', 'group')

    def user_can_access(self, user):
        if self.group in user.groups.all():
            return True
        return False

    def __str__(self):
        return "Le group %s peut voir l'album" % self.group.name


class EventAccess(AccessPolicy):
    event = models.ForeignKey(Event)

    class Meta:
        unique_together = ('path', 'event')

    def user_can_access(self, user):
        try:
            inscription = Inscription.objects.get(user=user, event=self.event)
            return bool(inscription.in_date)
        except Inscription.DoesNotExist:
            return False

    def __str__(self):
        return "Les participants de l'évennement %s peuvent voir l'abum" % self.event.name

