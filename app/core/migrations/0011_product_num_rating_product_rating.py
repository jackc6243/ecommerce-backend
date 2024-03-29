# Generated by Django 5.0.1 on 2024-01-16 09:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_product_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='num_rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='rating',
            field=models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)]),
        ),
    ]
