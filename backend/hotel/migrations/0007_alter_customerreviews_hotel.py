# Generated by Django 5.1 on 2024-12-03 01:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0006_alter_customerreviews_rating_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerreviews',
            name='hotel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='hotel.hotel'),
        ),
    ]
