from django.test import TestCase

# Create your tests here.
from django.utils.datetime_safe import datetime
from sharing.models import Bijdrage


class BijdrageTests(TestCase):
    def setUp(self):
        pass

    def test_bijdrage_can_be_x(self):
        bij = Bijdrage()

        bij.soort = 1
        bij.datum = datetime.now()
        bij.event_id = 1
        bij.user_id = 1
        try:
            bij.save()
            self.assertIsNotNone(bij.pk)
        except:
            self.assertEqual(True, False, 'Could not save bijdrage with valid inputs')
