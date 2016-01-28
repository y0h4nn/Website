from django.db import models
from django.contrib.auth.models import  Group
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Asso(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    mail = models.EmailField()
    members_group = models.ForeignKey(Group, related_name="asso_set", null=True, blank=True, on_delete=models.PROTECT)
    admins_group = models.ForeignKey(Group, related_name="asso_admin_set", null=True, blank=True, on_delete=models.PROTECT)
    site = models.URLField(null=True, blank=True)
    picture = models.ImageField(upload_to="asso_pictures", null=True, blank=True)

    class Meta:
        permissions = (
            ('manage_asso', 'Can manage associations'),
        )

    def __str__(self):
        return self.name

    def user_is_admin(self, user):
        return self.admins_group in user.groups.all() or user.has_perm('asso.manage_asso')


@receiver(pre_save, sender=Asso)
def auto_create_groups(sender, instance, **kwargs):
    if not instance.admins_group:
        admins_group_name = "asso_admins_%s" % instance.name.replace(' ', '_')
        admins_group, created = Group.objects.get_or_create(name=admins_group_name)
        instance.admins_group = admins_group

    if not instance.members_group:
        members_group_name = "asso_members_%s" % instance.name.replace(' ', '_')
        members_group, created = Group.objects.get_or_create(name=members_group_name)
        instance.members_group = members_group
