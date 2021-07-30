from django.test import TestCase
from django.utils import timezone
from model_mommy import mommy

from stranger_parties.invite.models import Guest, Event, Invite


class GuestTestCase(TestCase):
    def setUp(self) -> None:
        self.guest = mommy.make(Guest)
        self.guest.first_name = "Jhon"
        self.guest.last_name = "Coltrane"
        self.guest.email = "coltranekyes@bigband.com"
        self.guest.save()

    def test_a_add_guest(self):
        self.assertIsNotNone(self.guest)
        self.assertIsNotNone(self.guest.email)
        self.assertGreater(Guest.objects.count(), 0)
        self.assertEqual(str(self.guest), "Jhon Coltrane")

    def test_b_bulk_create(self):
        mommy.make(Guest, _quantity=100)
        self.assertEqual(Guest.objects.count(), 101)

    def test_c_update_guest(self):
        new_first_name = "Jacco"
        new_last_name = "Pastorius"
        new_email = "jaccobass@bigband.com"

        self.guest.email = new_email
        self.guest.first_name = new_first_name
        self.guest.last_name = new_last_name
        self.guest.save()

        self.assertEqual(self.guest.first_name, new_first_name)
        self.assertEqual(self.guest.last_name, new_last_name)
        self.assertEqual(self.guest.email, new_email)

    def test_d_user_properties(self):
        self.assertIsNotNone(self.guest.email)
        self.assertIsNotNone(self.guest.first_name)
        self.assertIsNotNone(self.guest.last_name)
        self.assertIsNotNone(self.guest.get_full_name())
        self.assertIsNotNone(self.guest.get_short_name())

        self.assertFalse(self.guest.is_staff)
        self.assertFalse(self.guest.last_login)
        self.assertTrue(self.guest.is_active)
        self.assertEqual(self.guest.EMAIL_FIELD, "email")
        self.assertEqual(self.guest.USERNAME_FIELD, "username")
        self.assertEqual(self.guest.REQUIRED_FIELDS, ["email"])

    def test_d_invite_guest(self):
        e = Event.objects.create(
            name="Aniversário do Guanabara", date_time=timezone.now()
        )
        Invite.objects.create(guest=self.guest, event=e)

        self.assertEqual(self.guest.total_invites, 1)
