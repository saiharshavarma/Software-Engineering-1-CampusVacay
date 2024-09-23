from django.contrib import admin
from .models import Hotel

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