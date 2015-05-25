from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

# Create your tests here.
from accounts.models import Account


class LoginViewTest(TestCase):
    def setUp(self):
        u = User(username='test', password='test')
        u.save()

    def test_login(self):
        r = self.client.post('/account/login/', {'username': 'test', 'password': 'test'}, follow=True)

        self.assertEqual(r.status_code, 200)

    def test_login_fails(self):
        r = self.client.post('/account/login/', {'username': 'test', 'password': 'test'}, follow=True)

        messages = list(r.context['messages'])

        self.assertTrue(messages)
        self.assertIn("klopt niet", messages[0].message)

    def test_login_deactivated(self):
        u = User(username='deactivated', password='test')
        u.is_active = False
        u.save()

        r = self.client.post('/account/login/', {'username': u.username, 'password': 'test'}, follow=True)

        self.assertEqual(r.status_code, 200)
        messages = list(r.context['messages'])

        self.assertTrue(messages)

    def test_logout(self):
        self.client.login(username='test', password='test')

        r = self.client.get('/account/logout/', follow=True)

        messages = list(r.context['messages'])

        self.assertTrue(messages)
        self.assertIn("Uitloggen",messages[0].message)

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

    def test_account_str_fails(self):
        u = User.objects.get(username='test')
        g = Account.objects.get(gebruiker=u)
        self.assertNotEqual('not test', str(g))


