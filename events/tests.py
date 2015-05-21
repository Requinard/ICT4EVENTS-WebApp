from django.test import TestCase
from django.contrib.auth.models import User, UserManager
from django.utils.timezone import datetime
from .models import *

# Create your tests here.
class AccountTests(TestCase):
    def setUp(self):
        u = User(username='test', password='test')
        u.save()

    def test_account_is_created(self):
        u = User.objects.get(username='test')
        g = Account.objects.get(gebruiker=u)

        self.assertIsNotNone(g, 'gebruiker gevonden')
        self.assertIsNot(g.activatiehash, '1')

    def test_account_is_deleted(self):
        u = User.objects.get(username='test')

        u.delete()

        g = Account.objects.filter(gebruiker=u)

        self.assertEqual(len(g), 0)

        g = Account.objects.filter(gebruiker__username='test')

        self.assertEqual(len(g), 0)

    def test_account_str(self):
        u = User.objects.get(username='test')
        g = Account.objects.get(gebruiker=u)
        self.assertEqual('test', str(g), 'Names do not match')

    def test_account_str(self):
        u = User.objects.get(username='test')
        g = Account.objects.get(gebruiker=u)
        self.assertNotEqual('not test', str(g))


class BijdrageTests(TestCase):
    def setUp(self):
        pass

    def test_bijdrage_can_be_x(self):
        b = Bijdrage().soort

        for item in b:
            bij = Bijdrage()

            bij.soort = item
            bij.datum = datetime.now()
            try:
                bij.save()
                self.assertIsNotNone(bij.pk)
            except:
                self.assertEqual(True, False, 'Could not save bijdrage with valid inputs')

    def test_bijdrage_cannot_be(self):
        b = Bijdrage()
        b.soort = "Dit kan nooit"
        b.datum = datetime.now()
        try:
            b.save()
            self.assertEqual(True, False, 'Managed to create bijdrage that cannot be')
        except:
            pass