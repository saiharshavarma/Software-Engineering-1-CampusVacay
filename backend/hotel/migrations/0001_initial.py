# Generated by Django 5.1 on 2024-09-23 00:43

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotel_name', models.CharField(max_length=255, verbose_name='Hotel Name')),
                ('address', models.TextField(verbose_name='Address')),
                ('phone_number', models.CharField(blank=True, max_length=12, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+19999999999'. It must have 10 digits after the country code.", regex='^\\+?1?\\d{10}$')], verbose_name='Phone Number')),
                ('description', models.TextField(blank=True, verbose_name='General Hotel Description')),
                ('facilities', models.CharField(blank=True, help_text='Provide a list of facilities such as pool, spa, parking, etc.', max_length=500, verbose_name='Other Facilities')),
                ('check_in_time', models.TimeField(default='15:00', verbose_name='Check-in Time')),
                ('check_out_time', models.TimeField(default='11:00', verbose_name='Check-out Time')),
                ('cancellation_policy', models.TextField(blank=True, verbose_name='Cancellation Policy')),
                ('student_discount', models.DecimalField(decimal_places=2, default=0.0, help_text='Percentage discount for students', max_digits=5, verbose_name='Student Discount (%)')),
                ('special_offers', models.CharField(blank=True, max_length=255, verbose_name='Special Offers')),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Added')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='hotel_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
