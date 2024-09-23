from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone
from django.core.exceptions import ValidationError

class Hotel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='hotel_profile')
    
    hotel_name = models.CharField(max_length=255, verbose_name='Hotel Name')
    address = models.TextField(verbose_name='Address')
    
    # Phone number with validation
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{10}$',
        message="Phone number must be entered in the format: '+19999999999'. It must have 10 digits after the country code."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=12, blank=True, verbose_name='Phone Number')
    
    # Hotel description and facilities
    description = models.TextField(verbose_name='General Hotel Description', blank=True)
    facilities = models.TextField(verbose_name='Facilities', help_text="Comma-separated list of facilities, e.g., Wi-Fi, Pool, Parking", blank=True)
    check_in_time = models.TimeField(verbose_name='Check-in Time', default="15:00")
    check_out_time = models.TimeField(verbose_name='Check-out Time', default="11:00")
    cancellation_policy = models.TextField(verbose_name='Cancellation Policy', blank=True)
    student_discount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Student Discount (%)', default=0.00, help_text="Percentage discount for students")
    special_offers = models.CharField(max_length=255, verbose_name='Special Offers', blank=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, verbose_name='Average Rating', blank=True, null=True)
    
    # Date when the hotel profile was added
    date_added = models.DateTimeField(default=timezone.now, verbose_name='Date Added')

    def __str__(self):
        return f'{self.hotel_name} - Student Profile'
    
    def clean(self):
        super().clean()

        if self.phone_number:
            phone_digits = self.phone_number.replace('+', '').replace(' ', '').replace('-', '')
            
            if len(phone_digits) == 10:
                self.phone_number = '+1' + phone_digits
            elif len(phone_digits) == 11 and phone_digits.startswith('1'):
                self.phone_number = '+' + phone_digits
            else:
                raise ValidationError("Phone number must have exactly 10 digits or start with '+1' followed by 10 digits.")