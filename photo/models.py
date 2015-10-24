from django.db import models
from django.contrib.auth.models import User, Group
from events.models import Inscription, Event



class AccessPolicy(models.Model):
    path = models.CharField(max_length=255)

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
    def user_can_access(self, user):
        return True

    def __str__(self):
        return "Tous le monde peut voir l'album"

class GroupAccess(AccessPolicy):
    group = models.ForeignKey(Group)

    def user_can_access(self, user):
        if self.group in user.groups.all():
            return True
        return False

    def __str__(self):
        return "Seul le group %s peut voir l'album" % self.group.name

class EventAccess(AccessPolicy):
    event = models.ForeignKey(Event)

    def user_can_access(self, user):
        try:
            inscription = Inscription.objects.get(user=user, event=event)
            return bool(inscription.in_date)
        except Inscription.DoesNotExists:
            return False

    def __str__(self):
        return "Seul les participants de l'évennement %s peuvent voir l'abum" % self.event.name

POLICIES = {
    'public': PublicAccess,
    'group': GroupAccess,
    'event': EventAccess,
}
