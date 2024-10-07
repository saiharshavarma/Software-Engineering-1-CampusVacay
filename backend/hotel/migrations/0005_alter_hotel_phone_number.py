# Generated by Django 5.1 on 2024-10-06 21:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0004_alter_customerreviews_hotel_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='phone_number',
            field=models.CharField(blank=True, max_length=12, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+19999999999'. It must have 10 digits after the country code.", regex='^\\+?1?\\d{10}$')], verbose_name='Phone Number'),
        ),
    ]