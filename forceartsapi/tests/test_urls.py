"""Module for unit tests"""
from django.test import TestCase
from django.urls import reverse


class TestUrls(TestCase):
    """Test application urls"""
    def test_category_url_resolved(self):
        """Checks category url"""
        response = self.client.get(reverse('category'))
        self.assertEquals(response.status_code, 200)

    def test_search_url_resolved(self):
        """Checks search url"""
        response = self.client.get(
            reverse('search'),
            {
                'limit': 20,
                'offset': 0,
                'query': '',
                'order': 'likes'
            }
        )
        self.assertEquals(response.status_code, 200)

    def test_contact_url_resolved(self):
        """Checks contact url"""
        response = self.client.post(
            reverse('contact-us'),
            {
                'full_name': 'Test Name',
                'email': 'test@gmail.com',
                'message': 'Test message',
            }
        )
        self.assertEquals(response.status_code, 201)
