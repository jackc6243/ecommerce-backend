"""
Tests for products api
"""

from datetime import date, timedelta

from django.test import TestCase
from core import models
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


ALL_URL = reverse('products:all_products')
NEW_URL = reverse('products:new')
DISCOUNT_URL = reverse('products:discounts')
FASHION_CATEGORY_URL = reverse(
    'products:category', kwargs={"category": "fashion"})


class ProductTests(TestCase):
    """Testing product api"""

    @classmethod
    def setUpTestData(self):
        """Setting up base data"""
        self.data_titles = []
        self.data_ids = []
        for i in range(5):
            product_info = {
                'title': f'sample product{i}',
                'description': f'blah blah blah {i}',
                'price': 4.9+i,
                'creation_date': date.today()-timedelta(days=26*i),
            }
            if i % 2 == 0:
                product_info['discount'] = 0.9-i*0.1
            if i % 3 == 0:
                product_info['category'] = 'fashion'
            instance = models.Product.objects.create(**product_info)
            instance.save()
            self.data_titles.append(instance.title)
            self.data_ids.append(instance.id)

        self.client = APIClient()

    def test_getting_all_products(self):
        """testing that getting all products work"""

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
        """test getting information on a single product"""
        SINGLE_PRODUCT_URL = reverse(
            'products:product', args=[self.data_ids[0]])
        res = self.client.get(SINGLE_PRODUCT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['title'], self.data_titles[0])
