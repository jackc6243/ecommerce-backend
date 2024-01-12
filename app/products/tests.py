"""
Tests for products api
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime, timedelta


ALL_URL = reverse('products:all_products')
NEW_URL = reverse('products:new')
DISCOUNT_URL = reverse('products:discounts')
FASHION_CATEGORY_URL = reverse(
    'products:category', kwargs={"category": "fashion"})
SINGLE_PRODUCT_URL = reverse('products:product', args=[1])


class ProductTests(TestCase):
    """Testing product api"""

    @classmethod
    def setUpTestData(self):
        """Setting up base data"""
        self.data_titles = []
        for i in range(5):
            product_info = {
                'title': f'sample product{i}',
                'description': 'blah blah blah {i}',
                'price': 4.9+i,
                'creation_date': datetime.now()-timedelta(days=26*i),
            }
            if i % 2 == 0:
                product_info['discount'] = 0.9-i*0.1
            if i % 3 == 0:
                product_info['category'] = 'fashion'
            instance = models.Product.objects.create(**product_info)
            instance.save()
            self.data_titles.append(instance.title)

        self.client = APIClient()

    def test_getting_all_products(self):
        """testing that getting all products work"""
        for i in range(5):
            product_info = {
                'title': f'sample product{i}',
                'description': 'blah blah blah {i}',
                'price': 4.9+i,
            }
            models.Product.objects.create(**product_info).save()

        res = self.client.get(ALL_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(len(res.data), 5)
        for i in range(5):
            self.assertEqual(res.data[i]['title'], self.data_titles[i])

    def test_retrieving_new_products(self):
        """Testing that new products are returned"""

        res = self.client.get(NEW_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(len(res.data), 3)

    def test_retrieving_discounted_products(self):
        """Testing retrieving discounted_products"""
        res = self.client.get(DISCOUNT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(len(res.data), 3)
        c = 0
        for i in range(5):
            if i % 2 == 0:
                self.assertEqual(res.data[c]['title'], self.data_titles[i])
                c += 1

    def test_retrieve_fashion_category(self):
        """Testing retrieving correct prodcuts in category"""
        res = self.client.get(FASHION_CATEGORY_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(len(res.data), 2)
        self.assertEqual(self.data_titles[0], res.data[0]['title'])
        self.assertEqual(self.data_titles[3], res.data[1]['title'])

    def test_retrieve_single_product(self):
        res = self.client.get(SINGLE_PRODUCT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['title'], self.data_titles[0])
