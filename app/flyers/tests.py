from django.test import TestCase
from core.models import Flyer
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

FLYER_CATEGORY_URL = reverse('flyers:category',
                             kwargs={"category": "sample-category"})


class TestFlyerView(TestCase):
    """Test the flyer category view"""

    def setUp(self):
        """Set up the test case"""
        self.client = APIClient()
        initial_object = {
            'title': 'sample flyer',
            'description': 'blah blah blah',
            'category': 'sample-category',
        }
        inst = Flyer.objects.create(**initial_object)
        inst.save()

    def test_flyer_category_view(self):
        """Test the flyer category view"""
        response = self.client.get(FLYER_CATEGORY_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'sample flyer')
        self.assertEqual(response.data[0]['description'], 'blah blah blah')
        self.assertEqual(response.data[0]['category'], 'sample-category')
