import os
from django.test import TestCase
from django.contrib.auth.models import User
from . import backends

class NormalAithTest(TestCase):
    def setUp(self):
        self.auth_backend = backends.NormalAuth()
        self.imap_backend = backends.ImapAuth()

        # Be carefull when changing user password ad they are hardcoded
        self.ext_user = User.objects.create_user('AAA', 'AAA@exemple.com', 'AAA')
        self.enib_user = User.objects.create_user('BBB', 'BBB@enib.fr', 'BBB')

    def test_auth_mail(self):
        auth_user = self.auth_backend.authenticate(email=self.ext_user.email, password='AAA')
        self.assertEqual(self.ext_user.username, auth_user.username)

    def test_auth_enib(self):
        # auth with username as it's the email adress without le @enib.fr
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
        self.assertIsNotNone(auth_user)
        self.assertEqual(auth_user.email, mail)


