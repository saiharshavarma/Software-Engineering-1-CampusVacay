from django.contrib import admin
from .models import Hotel, RoomsDescription, CustomerReviews, Reservation

class HotelAdmin(admin.ModelAdmin):
    list_display = ('get_user_id', 'hotel_name', 'get_email', 'phone_number', 'address1', 'average_rating')

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

class RoomsDescriptionAdmin(admin.ModelAdmin):
    list_display = (
        'hotel', 
        'room_type', 
        'number_of_rooms', 
        'price_per_night', 
        'facilities', 
        'breakfast_included', 
        'room_size', 
        'max_occupancy', 
        'smoking_allowed'
    )
    search_fields = ('hotel__hotel_name', 'room_type')
    list_filter = ('breakfast_included', 'smoking_allowed', 'max_occupancy')

admin.site.register(RoomsDescription, RoomsDescriptionAdmin)
admin.site.register(Reservation)
admin.site.register(CustomerReviews)
admin.site.register(Hotel, HotelAdmin)