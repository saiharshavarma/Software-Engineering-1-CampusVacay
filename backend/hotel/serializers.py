from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Hotel, add_user_to_hotel_group, RoomsDescription, Reservation

class UserRegistrationSerializer(serializers.ModelSerializer):
    hotel_name = serializers.CharField(max_length=255, required=True)
    phone_number = serializers.CharField(max_length=12, required=True)
    address = serializers.CharField(style={'base_template': 'textarea.html'}, required=True)
    location =serializers.CharField(style={'base_template': 'textarea.html'}, required=False, allow_blank=True)
    city = serializers.CharField(style={'base_template': 'textarea.html'}, required=True)
    country = serializers.CharField(style={'base_template': 'textarea.html'}, required=True)
    hotel_photos = serializers.FileField(required=True, allow_empty_file=False, write_only=True)
    description = serializers.CharField(style={'base_template': 'textarea.html'}, required=False, allow_blank=True)
    facilities = serializers.CharField(style={'base_template': 'textarea.html'}, required=False, allow_blank=True)
    check_in_time = serializers.TimeField(default="15:00")
    check_out_time = serializers.TimeField(default="11:00")
    cancellation_policy = serializers.CharField(style={'base_template': 'textarea.html'}, required=False, allow_blank=True)
    student_discount = serializers.DecimalField(max_digits=5, decimal_places=2, required=False, default=0.00)
    special_offers = serializers.CharField(max_length=255, required=False, allow_blank=True)


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
            'room', 'student', 'first_name', 'last_name', 'email',
            'country', 'phone_number', 'expected_arrival_time', 
            'special_requests', 'payment_mode', 'check_in_date', 
            'check_out_date', 'guests'
        ]

    def validate(self, data):
        # Ensure check-out date is after check-in date
        if data['check_out_date'] <= data['check_in_date']:
            raise serializers.ValidationError("Check-out date must be after check-in date.")
        
        # Optional: Add logic to check room availability

        return data
    
class ReservationListSerializer(serializers.ModelSerializer):
    hotel_name = serializers.CharField(source='room.hotel.hotel_name', read_only=True)
    room_type = serializers.CharField(source='room.room_type', read_only=True)

    class Meta:
        model = Reservation
        fields = [
            'id', 'hotel_name', 'room_type', 'check_in_date', 'check_out_date', 
            'guests', 'booking_date', 'first_name', 'last_name', 'email', 
            'expected_arrival_time', 'special_requests', 'payment_mode'
        ]

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