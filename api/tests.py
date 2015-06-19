from django.test import TestCase

from events.models import Plek, PlekSpecificatie, Locatie, Specificatie



# Create your tests here.
class PlekViewsetTest(TestCase):
    l = Locatie()
    p = Plek()

    def setUp(self):
        l = Locatie(naam="testing")
        l.save()

        self.l = l

        p = Plek()
        p.locatie = l

        p.save()

        self.p = p

    def test_view(self):
        res = self.client.get('/api/plek/%s/' % (str(self.p.pk)), follow=True)

        self.assertEqual(res.content, b'{"id":1,"nummer":null,"capaciteit":null,"locatie":1}', "JSON did not equal")

    def test_view_404(self):
        res = self.client.get('/api/plek/%s/' % (str(13200320123)), follow=True)

        self.assertEqual(res.status_code, 404, "Accidentally found some data")


class PlekAutocompleteViewset(TestCase):
    l = Locatie()
    p = Plek()

    def setUp(self):
        l = Locatie(naam="testing")
        l.save()

        self.l = l

        p = Plek()
        p.locatie = l

        p.save()

        self.p = p

        s = Specificatie()

        s.naam = "test"

        s.save()

        ps = PlekSpecificatie()

        ps.plek = p
        ps.specificatie = s

        ps.save()

    def _nw_test_view(self):
        res = self.client.get('/api/auto/plek/%s/' % (str(self.p.nummer)), follow=True)

        print('/api/auto/plek/%s/' % (str(p.nummer)))
        print(res.content)

        self.assertEqual(res.content, b'{"id":1,"nummer":null,"capaciteit":null,"locatie":1}', "JSON did not equal")
