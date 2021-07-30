from django.test import TestCase
from model_mommy import mommy

from stranger_parties.invite.models import Event


class EventTestCase(TestCase):
    def test_a_add_guest(self):
        mommy.make(Event, _quantity=100)
