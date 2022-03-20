"""Module for unit tests"""
from django.test import TestCase
from forceartsapi.models import ContactUs


class TestModels(TestCase):
    """Tests application models"""
    def setUp(self) -> None:
        """Initializes models"""
        ContactUs.objects.create(
            full_name="Shukhrat Mirrakhimov",
            email="shukhrat.mirrakhimov@test.com",
            message="Hello World!"
        )

    def test_contact_object(self):
        """Checks contact object field values"""
        contact = ContactUs.objects.get(email="shukhrat.mirrakhimov@test.com")
        self.assertEqual(contact.full_name, "Shukhrat Mirrakhimov")
        self.assertEqual(contact.email, "shukhrat.mirrakhimov@test.com")
        self.assertEqual(contact.message, "Hello World!")
