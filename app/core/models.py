"""
Database models
"""
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from datetime import date
from django.db import models
import uuid
import os


def product_image_file_path(instance, filename):
    """Generate file path for new product image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads', 'products', filename)


def flyer_image_file_path(instance, filename):
    """Generate file path for new flyer image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads', 'flyers', filename)


class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Creating a superuser"""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class Product(models.Model):
    """Product model"""
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    category = models.CharField(max_length=255, default='technology')
    price = models.FloatField()
    discount = models.FloatField(default=1.0)
    creation_date = models.DateField(default=date.today)
    alt = models.TextField(max_length=255, default='product')
    image = models.ImageField(
        null=True,
        upload_to=product_image_file_path)

    # objects = productManager()

    def __str__(self):
        return self.title


class User(AbstractBaseUser, PermissionsMixin):
    """User model"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    favorites = models.ManyToManyField(Product, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Flyer(models.Model):
    """Images and names of flyers"""
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=255, default='main')
    image = models.ImageField(
        null=True,
        upload_to=flyer_image_file_path)

    def __str__(self):
        return self.title
