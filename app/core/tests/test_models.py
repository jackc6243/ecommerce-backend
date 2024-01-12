"""
Tests for models
"""
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
        }

        product = models.Product.objects.create(**product_info)
        self.assertEqual(product.title, product_info['title'])
        self.assertEqual(product.price, product_info['price'])

    # def test_add_to_favorites(self):
    #     """Testing can add a product to favorites"""
    #     user = get_user_model().objects.create_user(
    #         'test@example.com',
    #         'password1234',
    #     )
    #     product = models.Product.objects.create(
    #         user=user,
    #         title='Sample title'
    #     )

    #     self.assertEqual(str(product), product.title)
