from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

# Create your tests here.
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

        print r.context

        self.assertTrue(messages)
        self.assertIn("Uitloggen",messages[0].message)

