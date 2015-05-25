from django.test import TestCase

# Create your tests here.
from django.utils.datetime_safe import datetime
from sharing.models import Bijdrage


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
        self.assertRaises(Exception, b.save())