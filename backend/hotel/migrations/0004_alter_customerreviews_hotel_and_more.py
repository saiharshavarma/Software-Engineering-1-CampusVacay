# Generated by Django 5.1 on 2024-09-23 01:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0003_customerreviews_roomsdescription'),
        ('student', '0003_alter_student_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerreviews',
            name='hotel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hotel_reviews', to='hotel.hotel'),
        ),
        migrations.AlterField(
            model_name='customerreviews',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_reviews', to='student.student'),
        ),
    ]
