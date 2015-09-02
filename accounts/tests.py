import os
from django.test import TestCase
from django.contrib.auth.models import User, Group
from . import backends


class NormalAuthTest(TestCase):
    fixtures = ["fixtures/groups"]

    def setUp(self):
        self.auth_backend = backends.NormalAuth()
        self.imap_backend = backends.ImapAuth()

        # Be careful when changing user passwords as they are hardcoded
        self.ext_user = User.objects.create_user('AAA', 'AAA@exemple.com', 'AAA')
        self.enib_user = User.objects.create_user('BBB', 'BBB@enib.fr', 'BBB')

    def test_auth_mail(self):
        auth_user = self.auth_backend.authenticate(email=self.ext_user.email, password='AAA')
        self.assertEqual(self.ext_user.username, auth_user.username)

    def test_auth_enib(self):
        # auth with username as it's the email adress without @enib.fr
        auth_user = self.auth_backend.authenticate(email=self.enib_user.username, password='BBB')
        self.assertEqual(self.enib_user.username, auth_user.username)

    def test_auth_reject(self):
        auth_user = self.auth_backend.authenticate(email='INVALID', password='INVALID')
        self.assertIsNone(auth_user)

    def test_auth_ext_no_full_mail(self):
        auth_user = self.auth_backend.authenticate(email=self.ext_user.username, password='CCC')
        self.assertIsNone(auth_user)

    def test_auth_wrong_passwd(self):
        auth_user = self.auth_backend.authenticate(email=self.enib_user.email, password='INVALID')
        self.assertIsNone(auth_user)

    def test_imap_enib_fail(self):
        auth_user = self.imap_backend.authenticate(email='INVALID@enib.fr', password='INVALID')
        self.assertIsNone(auth_user)

    def test_imap_enib_success(self):
        try:
            mail = os.environ['test_mail']
            password = os.environ['test_password']
        except:
            mail = password = None
        auth_user = self.imap_backend.authenticate(email=mail, password=password)
        groups = auth_user.groups.all()
        self.assertIsNotNone(auth_user)
        self.assertEqual(auth_user.email, mail)
        self.assertEqual(groups[0].name, "Tous")
        self.assertEqual(groups[1].name, "Enib")

    def test_imap_enib_success_with_space(self):
        try:
            mail = os.environ['test_mail'] + " "
            password = os.environ['test_password']
        except:
            mail = password = None
        auth_user = self.imap_backend.authenticate(email=mail, password=password)
        groups = auth_user.groups.all()
        self.assertIsNotNone(auth_user)
        self.assertEqual(auth_user.email, mail.strip())
        self.assertEqual(groups[0].name, "Tous")
        self.assertEqual(groups[1].name, "Enib")


class ProfilTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('AAA', 'AAA@exemple.com', 'AAA')

    def test_only_nickname(self):
        self.user.profile.nickname = "Test"
        self.user.profile.save()
        self.assertEqual(str(self.user.profile), "Test")

    def test_only_first_name(self):
        self.user.first_name = "first_name"
        self.user.profile.save()
        self.assertEqual(str(self.user.profile), "AAA")

    def test_only_last_name(self):
        self.user.first_name = "last_name"
        self.user.profile.save()
        self.assertEqual(str(self.user.profile), "AAA")

    def test_last_name_and_first_name(self):
        self.user.last_name = "last_name"
        self.user.first_name = "first_name"
        self.user.save()
        self.assertEqual(str(self.user.profile), "first_name last_name")

    def test_all_names(self):
        self.user.last_name = "last_name"
        self.user.first_name = "first_name"
        self.user.save()
        self.user.profile.nickname = "Test"
        self.assertEqual(str(self.user.profile), "first_name « Test » last_name")

    def test_last_name_and_nickname(self):
        self.user.profile.nickname = "Test"
        self.user.profile.save()
        self.user.last_name = "last_name"
        self.user.save()
        self.assertEqual(str(self.user.profile), "Test")

    def test_first_name_and_nickname(self):
        self.user.profile.nickname = "Test"
        self.user.profile.save()
        self.user.first_name = "last_name"
        self.user.save()
        self.assertEqual(str(self.user.profile), "Test")

