from django.db import models
from django.contrib.auth.models import User, Group
from student.models import Student
from django.core.validators import RegexValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import migrations
from django.contrib.postgres.fields import JSONField
import json
from decimal import Decimal

def create_hotel_group(apps, schema_editor):
    Group.objects.get_or_create(name='Hotels')

class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(create_hotel_group),
    ]

def add_user_to_hotel_group(user):
    hotel_group, created = Group.objects.get_or_create(name='Hotels')
    user.groups.add(hotel_group)

class Hotel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='hotel_profile')
    
    hotel_name = models.CharField(max_length=255, verbose_name='Hotel Name')
    address1 = models.TextField(verbose_name='Address1')
    address2 = models.TextField(verbose_name='Address2', blank=True, null=True)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="N/A")
    zip = models.IntegerField()
    hotel_photos = models.FileField(upload_to='hotel_photos/', verbose_name='Hotel Photos', help_text="Upload an image file", null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    tourist_spots = models.JSONField(default=list) 
    
    # Phone number with validation
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{10}$',
        message="Phone number must be entered in the format: '+19999999999'. It must have 10 digits after the country code."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=12, blank=True, verbose_name='Phone Number', unique=True)
    
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
        return f'{self.hotel_name} - Hotel Profile'

# Rooms_Description model for managing different room types for each hotel           
class RoomsDescription(models.Model):
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE, related_name='rooms')

    # Room type and general information
    room_type = models.CharField(max_length=255, verbose_name='Room Type')
    number_of_rooms = models.IntegerField(verbose_name='Number of Rooms')

    # Pricing and facilities
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Price per Night (USD)')
    facilities = models.TextField(
        verbose_name='Room Facilities', 
        help_text="Comma-separated list of room facilities, e.g., Wi-Fi, TV, Mini-bar, Sea View"
    )
    breakfast_included = models.BooleanField(default=False, verbose_name='Breakfast Included')
    
    # Additional room features
    room_size = models.CharField(max_length=50, verbose_name='Room Size (e.g., 30 sqm)', blank=True)
    max_occupancy = models.IntegerField(verbose_name='Maximum Occupancy', help_text="Number of guests allowed", blank=True, null=True)
    smoking_allowed = models.BooleanField(default=False, verbose_name='Smoking Allowed')

    def __str__(self):
        return f'{self.hotel.hotel_name} - {self.room_type}'

class FinalReservation(models.Model):
    currency = models.CharField(max_length=3, default='usd')
    stripe_payment_id = models.CharField(max_length=100, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    payment_status = models.CharField(max_length=20, choices=[('succeeded', 'succeeded'), ('failed', 'failed')], default='failed')

    def __str__(self):
        return f"FinalReservation {self.id} - {self.hotel.hotel_name}"    
class Reservation(models.Model):
    reservation = models.ForeignKey(FinalReservation, on_delete=models.CASCADE, null = True, blank=True, related_name='hotel_reservations')  
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_reservations')
    room = models.ForeignKey(RoomsDescription, on_delete=models.CASCADE, related_name='room_reservations')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_reservations')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    country = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    expected_arrival_time = models.TimeField(blank = True, null = True)
    special_requests = models.TextField(blank=True, null=True)

    payment_mode = models.CharField(max_length=50, choices=[('card', 'Card'), ('cash', 'Cash')], default='card')
    damage_insurance = models.BooleanField(default=False)
    stripe_payment_id = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='usd')
    payment_status = models.CharField(max_length=20, choices=[('succeeded', 'succeeded'), ('failed', 'failed')], default='failed')

    check_in_date = models.DateField()
    check_out_date = models.DateField()
    guests = models.IntegerField()
    booking_date = models.DateTimeField(auto_now_add=True)

    room_number = models.CharField(max_length=10, blank=True, null=True)  # Room number on check-in
    checked_in = models.BooleanField(default=False)  # Check-in status
    additional_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Track extra charges
    damage_report = models.TextField(blank=True, null=True)

    # New fields for cancellation logic
    canceled = models.BooleanField(default=False)
    cancellation_date = models.DateTimeField(blank=True, null=True)
    cancellation_reason = models.TextField(blank=True, null=True)
    
    def __str__(self):
        status = "Canceled" if self.canceled else "Active"
        return f"Reservation ({status}) - {self.room.hotel.hotel_name} - {self.room.room_type}"

    def clean(self):
        if self.check_out_date <= self.check_in_date:
            raise ValidationError("Check-out date must be after check-in date.")
        
    def cancel(self, reason=None):
        """Cancel the booking and record the reason."""
        self.canceled = True
        self.cancellation_date = timezone.now()
        self.cancellation_reason = reason
        self.save()

    def calculate_cost(self):
        duration = (self.check_out_date - self.check_in_date).days
        if duration <= 0:
            raise ValueError("The duration of the stay must be at least one night.")

        # Convert room price to Decimal and calculate base cost
        base_cost = Decimal(duration) * self.room.price_per_night

        # Convert hotel discount to Decimal and apply it
        hotel_discount = Decimal(self.hotel.student_discount) / Decimal(100)
        discounted_cost = base_cost * (Decimal(1) - hotel_discount)

        # Calculate insurance cost if applicable
        if self.damage_insurance:
            insurance_rate = Decimal(0.05)  # 5% extra for insurance
            total_cost = discounted_cost * (Decimal(1) + insurance_rate)
        else:
            total_cost = discounted_cost

        return total_cost
    

    
# CustomerReviews model for storing reviews from students
class CustomerReviews(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='reviews')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_reviews')
    rating = models.PositiveSmallIntegerField(verbose_name='Rating', help_text="Rate between 1 to 5 stars", default=0)
    review = models.TextField(verbose_name='Review', blank=True, default="")
    date_added = models.DateTimeField(default=timezone.now, verbose_name='Date Added')

    def __str__(self):
        return f'Review by {self.student.user.username} for {self.hotel.hotel_name} - {self.rating} stars on {self.date_added}'
    
    def save(self, *args, **kwargs):
    # Call the original save method to save the review
        super().save(*args, **kwargs)

        # Update the average rating of the associated hotel
        reviews = self.hotel.reviews.all()
        average_rating = reviews.aggregate(models.Avg('rating'))['rating__avg']
        self.hotel.average_rating = round(average_rating, 2)  # Round to 2 decimal places
        self.hotel.save()