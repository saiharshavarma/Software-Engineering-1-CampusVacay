from django.contrib import admin
from .models import Student

class StudentAdmin(admin.ModelAdmin):
    list_display = ('get_user_id', 'get_full_name', 'university_name', 'get_username', 'get_email', 'phone_number')

    def get_user_id(self, obj):
        return obj.user.id
    get_user_id.short_description = 'User ID'

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_full_name.short_description = 'Full Name'

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

    def university_name(self, obj):
        return obj.university_name
    university_name.short_description = 'University'

    def phone_number(self, obj):
        return obj.phone_number
    phone_number.short_description = 'Phone Number'

admin.site.register(Student, StudentAdmin)