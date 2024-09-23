from django.contrib import admin
from django.db import migrations
from django.contrib.auth.models import Group
from .models import Hotel

from django.db import migrations
from django.contrib.auth.models import Group

def create_hotel_group(apps, schema_editor):
    Group.objects.get_or_create(name='Hotels')

class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(create_hotel_group),
    ]

def add_user_to_hotel_group(user):
    hotel_group, created = Group.objects.get_or_create(name='Hotels')
    user.groups.add(hotel_group)

class HotelAdmin(admin.ModelAdmin):
    list_display = ('get_user_id', 'hotel_name', 'get_email', 'phone_number', 'address', 'average_rating')

    def get_user_id(self, obj):
        return obj.user.id
    get_user_id.short_description = 'User ID'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

    def phone_number(self, obj):
        return obj.phone_number
    phone_number.short_description = 'Phone Number'

    def average_rating(self, obj):
        return obj.average_rating
    average_rating.short_description = 'Average Rating'

admin.site.register(Hotel, HotelAdmin)