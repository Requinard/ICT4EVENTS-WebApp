from django.test import TestCase
from django.contrib.auth.models import User, UserManager

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