"""
Tests for models
"""
from datetime import date
from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """Can create user with email"""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalised(self):
        """Test email is normalised when user created"""

        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Creating user without email raises value error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser"""
        user = get_user_model().objects.create_superuser(
            email='test@example.com',
            password='test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_new_product(self):
        """Test creating new product"""

        product_info = {
            'title': 'sample product',
            'description': 'blah blah blah',
            'price': 4.9,
            'category': 'test_category',
            'discount': 0.4,
            'creation_date': date(2019, 4, 3),
        }

        product = models.Product.objects.create(**product_info)
        self.assertEqual(product.title, product_info['title'])
        self.assertEqual(product.price, product_info['price'])
        self.assertEqual(product.description, product_info['description'])
        self.assertEqual(product.category, product_info['category'])
        self.assertEqual(product.discount, product_info['discount'])
        self.assertEqual(product.creation_date, product_info['creation_date'])

    @patch('core.models.uuid.uuid4')
    def test_product_file_name_uuid(self, mock_uuid):
        """Test image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.product_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/products/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)

    def test_create_new_flyer(self):
        """Test creating new flyer"""
        flyer_info = {
            'title': 'sample flyer',
            'description': 'blah blah blah',
            'category': 'sample-category'
        }

        flyer = models.Flyer.objects.create(**flyer_info)

        self.assertEqual(flyer.title, flyer_info['title'])
        self.assertEqual(flyer.description, flyer_info['description'])
        self.assertEqual(flyer.category, flyer_info['category'])

    @patch('core.models.uuid.uuid4')
    def test_flyer_file_name_uuid(self, mock_uuid):
        """Test image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.flyer_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/flyers/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)

    def test_add_to_favorites(self):
        """Testing can add a product to favorites"""
        product_infos = [{
            'title': f'sample product{i}',
            'description': 'blah blah blah',
            'price': 4.9,
            'category': 'test_category',
            'discount': 0.4,
            'creation_date': date(2019, 4, 3),
        } for i in range(3)]

        user = get_user_model().objects.create_user(
            'test@example.com',
            'password1234',
        )

        for product_info in product_infos:
            product = models.Product.objects.create(**product_info)
            user.favorites.add(product)

        for i, favorite in enumerate(user.favorites.all()):
            self.assertEqual(product_infos[i]['title'], favorite.title)
