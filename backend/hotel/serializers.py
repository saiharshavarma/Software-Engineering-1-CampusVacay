from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Hotel, add_user_to_hotel_group, RoomsDescription, Reservation, CustomerReviews
import re

class UserRegistrationSerializer(serializers.ModelSerializer):
    hotel_name = serializers.CharField(max_length=255, required=True, write_only=True)
    phone_number = serializers.CharField(max_length=12, required=True, write_only=True)
    address = serializers.CharField(style={'base_template': 'textarea.html'}, required=True, write_only=True)
    location =serializers.CharField(style={'base_template': 'textarea.html'}, required=False, allow_blank=True, write_only=True)
    city = serializers.CharField(style={'base_template': 'textarea.html'}, required=True, write_only=True)
    country = serializers.CharField(style={'base_template': 'textarea.html'}, required=True, write_only=True)
    hotel_photos = serializers.FileField(required=True, allow_empty_file=False, write_only=True)
    description = serializers.CharField(style={'base_template': 'textarea.html'}, required=False, allow_blank=True, write_only=True)
    facilities = serializers.CharField(style={'base_template': 'textarea.html'}, required=False, allow_blank=True, write_only=True)
    check_in_time = serializers.TimeField(default="15:00", write_only=True)
    check_out_time = serializers.TimeField(default="11:00", write_only=True)
    cancellation_policy = serializers.CharField(style={'base_template': 'textarea.html'}, required=False, allow_blank=True, write_only=True)
    student_discount = serializers.DecimalField(max_digits=5, decimal_places=2, required=False, default=0.00, write_only=True)
    special_offers = serializers.CharField(max_length=255, required=False, allow_blank=True, write_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'password', 'email',
            'hotel_name', 'phone_number', 'address', 'location', 'city', 'country', 'hotel_photos', 'description', 'facilities',
            'check_in_time', 'check_out_time', 'cancellation_policy',
            'student_discount', 'special_offers'
        ]

    def create(self, validated_data):
        # Extract related fields for the Hotel profile
        hotel_name = validated_data.pop('hotel_name')
        phone_number = validated_data.pop('phone_number')
        address = validated_data.pop('address')
        location = validated_data.pop('location')
        city = validated_data.pop('city')
        country = validated_data.pop('country')
        hotel_photos = validated_data.pop('hotel_photos')
        description = validated_data.pop('description')
        facilities = validated_data.pop('facilities')
        check_in_time = validated_data.pop('check_in_time')
        check_out_time = validated_data.pop('check_out_time')
        cancellation_policy = validated_data.pop('cancellation_policy')
        student_discount = validated_data.pop('student_discount')
        special_offers = validated_data.pop('special_offers')

        # Create User object
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )

        # Add user to "Hotel" group
        add_user_to_hotel_group(user)

        # Create Hotel profile linked to the User
        hotel = Hotel.objects.create(
            user=user,
            hotel_name=hotel_name,
            phone_number=phone_number,
            address=address,
            location=location,
            city=city,
            country=country,
            hotel_photos=hotel_photos,
            description=description,
            facilities=facilities,
            check_in_time=check_in_time,
            check_out_time=check_out_time,
            cancellation_policy=cancellation_policy,
            student_discount=student_discount,
            special_offers=special_offers
        )
        hotel.full_clean()
        hotel.save()
        return user
    
    def validate_phone_number(self, value):
        # Check if the phone number is in the format +1 followed by 10 to 12 digits or just 10 to 12 digits without +1
        if not re.fullmatch(r'(\+1)?\d{10,12}$', value):
            raise serializers.ValidationError("Phone number must be in the format +1 followed by 10 to 12 digits, or just 10 to 12 digits.")
        return value

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomsDescription
        fields = '__all__'

class HotelSerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = [
            'hotel', 'room', 'student', 'first_name', 'last_name', 'email',
            'country', 'phone_number', 'expected_arrival_time', 
            'special_requests', 'payment_mode', 'check_in_date', 
            'check_out_date', 'guests'
        ]

    def validate(self, data):
        check_in_date = data.get('check_in_date')
        check_out_date = data.get('check_out_date')
        
        if not check_in_date or not check_out_date:
            raise serializers.ValidationError({
                'check_in_date': 'Check-in date is required.' if not check_in_date else '',
                'check_out_date': 'Check-out date is required.' if not check_out_date else ''
            })

        if check_out_date <= check_in_date:
            raise serializers.ValidationError(
                f"Check-out date ({check_out_date}) must be after check-in date ({check_in_date})."
            )


        return data
    
    def create(self, validated_data):
        reservation = super().create(validated_data)
        reservation.amount = reservation.calculate_cost()
        reservation.save()
        return reservation
    
class ReservationListSerializer(serializers.ModelSerializer):
    hotel_name = serializers.CharField(source='room.hotel.hotel_name', read_only=True)
    room_type = serializers.CharField(source='room.room_type', read_only=True)

    class Meta:
        model = Reservation
        fields = "__all__"

class ReservationDetailSerializer(serializers.ModelSerializer):
    hotel_name = serializers.CharField(source='room.hotel.hotel_name', read_only=True)
    room_type = serializers.CharField(source='room.room_type', read_only=True)

    class Meta:
        model = Reservation
        fields = [
            'id', 'hotel_name', 'room_type', 'first_name', 'last_name', 'email', 
            'phone_number', 'expected_arrival_time', 'special_requests', 'payment_mode',
            'check_in_date', 'check_out_date', 'guests', 'room_number', 'checked_in', 
            'additional_charges', 'canceled', 'cancellation_date', 'cancellation_reason'
        ]
        
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerReviews
        fields = "__all__"
        read_only_fields = ['hotel', 'student']