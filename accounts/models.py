from core.cache import invalid_cache
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.templatetags.static import static
from webmail.models import WebmailSettings


SEMESTERS = [(None, 'Aucun'), ]
SEMESTERS += [('S{}'.format(i), 'Semestre {}'.format(i)) for i in range(1, 11)]


class Family(models.Model):
    name = models.CharField(max_length=255)
    descriptionn = models.TextField(null=True, blank=True)
    picture = models.ImageField(height_field='height', width_field='width', null=True, blank=True)


class Promo(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    picture = models.ImageField(height_field='height', width_field='width', null=True, blank=True)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    nickname = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
    picture = models.ImageField(upload_to="profile_pictures", null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    family = models.ForeignKey('Family', related_name='members', null=True, blank=True)
    promo = models.ForeignKey('Promo', related_name='members', null=True, blank=True)
    enib_join_year = models.PositiveSmallIntegerField(null=True, blank=True)
    semester = models.CharField(max_length=3, choices=SEMESTERS, null=True, blank=True)

    def __str__(self):
        if self.user.first_name and self.user.last_name and self.user.profile.nickname:
            display_name_tpl = "{first_name} « {nickname} » {last_name}"
        elif self.user.first_name and self.user.last_name:
            display_name_tpl = "{first_name} {last_name}"
        elif self.user.profile.nickname:
            display_name_tpl = "{nickname}"
        else:
            display_name_tpl = "{uid}"

        return display_name_tpl.format(
            first_name=self.user.first_name,
            last_name=self.user.last_name,
            nickname=self.user.profile.nickname,
            uid=self.user.username,
        )

    def get_picture_url(self):
        if self.picture:
            return self.picture.url
        else:
            return static('images/default_user_icon.png')

    def get_url(self):
        return reverse('accounts:show', kwargs={'username': self.user.username})

    def is_valid(self):
        # We need to force fetch the object because django doesn't update it soon enough when we submit the edit form.
        prof = self.__class__.objects.get(id=self.id)
        return bool(prof.nickname or (prof.user.first_name and prof.user.last_name))


class Email(models.Model):
    email = models.EmailField()
    profile = models.ForeignKey('Profile', related_name='secondary_emails')
    valid = models.BooleanField(default=False)


class Address(models.Model):
    profile = models.OneToOneField('Profile', related_name='address')
    street = models.CharField(max_length=512, null=True, blank=True)
    postal_code = models.IntegerField(null=True, blank=True)
    town = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return "{}, {} {}".format(self.streer, self.postal_code, self.town)


class UserRequest(models.Model):
    email = models.EmailField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    class Meta:
        permissions = (
            ('manage_account_request', 'Can manage account request'),
        )

    def __str__(self):
        return self.username


@receiver(post_save, sender=User)
def create_favorites(sender, instance, created, **kwargs):
    updated = kwargs['update_fields']
    if updated != frozenset({'last_login'}):
        invalid_cache("members")
    if created:
        p = Profile.objects.create(user=instance)
        Address.objects.create(profile=p)
        WebmailSettings.objects.create(user=instance)
        all_group = Group.objects.get(name='Tous')
        all_group.user_set.add(instance)


@receiver(post_save, sender=Profile)
def cache_profile_handler(sender, **kwargs):
    invalid_cache("members")

