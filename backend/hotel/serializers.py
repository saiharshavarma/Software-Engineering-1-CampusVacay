from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Hotel, add_user_to_hotel_group


class UserRegistrationSerializer(serializers.ModelSerializer):
    hotel_name = serializers.CharField(max_length=255, required=True)
    phone_number = serializers.CharField(max_length=12, required=True)
    address = serializers.CharField(style={'base_template': 'textarea.html'}, required=True)
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
            'hotel_name', 'phone_number', 'address', 'description', 'facilities',
            'check_in_time', 'check_out_time', 'cancellation_policy',
            'student_discount', 'special_offers'
        ]

    def create(self, validated_data):
        # Extract related fields for the Hotel profile
        hotel_name = validated_data.pop('hotel_name')
        phone_number = validated_data.pop('phone_number')
        address = validated_data.pop('address')
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

        # Add user to "Students" group
        add_user_to_hotel_group(user)

        # Create Student profile linked to the User
        hotel = Hotel.objects.create(
            user=user,
            hotel_name=hotel_name,
            phone_number=phone_number,
            address=address,
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
