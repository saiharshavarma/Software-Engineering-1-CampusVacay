from django import forms
from django.contrib.auth.models import User
from .models import Hotel

class HotelRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    email = forms.EmailField(required=True)

    # Hotel-specific fields
    hotel_name = forms.CharField(max_length=255, required=True)
    phone_number = forms.CharField(max_length=12, required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)
    location = forms.CharField(widget=forms.Textarea, required=False)
    city = forms.CharField(widget=forms.Textarea, required=True)
    country = forms.CharField(widget=forms.Textarea, required=True)
    hotel_photos = forms.FileField(required=True)
    description = forms.CharField(widget=forms.Textarea, required=False)
    facilities = forms.CharField(widget=forms.Textarea, required=False)
    check_in_time = forms.TimeField(required=True, initial="15:00")
    check_out_time = forms.TimeField(required=True, initial="11:00")
    cancellation_policy = forms.CharField(widget=forms.Textarea, required=False)
    student_discount = forms.DecimalField(max_digits=5, decimal_places=2, required=False, initial=0.00)
    special_offers = forms.CharField(max_length=255, required=False)

    class Meta:
        model = Hotel
        fields = [
            'hotel_name', 'phone_number', 'address', 'location' , 'city', 'country', 'hotel_photos', 'description', 'facilities',
            'check_in_time', 'check_out_time', 'cancellation_policy', 
            'student_discount', 'special_offers'
        ]

class HotelLoginForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

    class Meta:
        model = Hotel
        fields = []