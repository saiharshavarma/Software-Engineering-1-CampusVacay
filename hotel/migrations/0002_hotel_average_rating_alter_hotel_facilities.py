# Generated by Django 5.1 on 2024-09-23 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='average_rating',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True, verbose_name='Average Rating'),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='facilities',
            field=models.TextField(blank=True, help_text='Comma-separated list of facilities, e.g., Wi-Fi, Pool, Parking', verbose_name='Facilities'),
        ),
    ]
