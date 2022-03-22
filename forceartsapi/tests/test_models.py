"""Module for unit tests"""
from django.test import TestCase
from django.contrib.auth import get_user_model
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

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@test.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@TEST.com'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@test.com',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_contact_object(self):
        """Checks contact object field values"""
        contact = ContactUs.objects.get(email="shukhrat.mirrakhimov@test.com")
        self.assertEqual(contact.full_name, "Shukhrat Mirrakhimov")
        self.assertEqual(contact.email, "shukhrat.mirrakhimov@test.com")
        self.assertEqual(contact.message, "Hello World!")
