from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Student, add_user_to_student_group
import re

class UserRegistrationSerializer(serializers.ModelSerializer):
    dob = serializers.DateField(write_only=True, input_formats=['%Y-%m-%d', '%m/%d/%Y', '%d-%m-%Y', '%Y/%m/%d'] )
    phone_number = serializers.CharField(write_only=True)
    address = serializers.CharField(write_only=True)
    university_name = serializers.CharField(write_only=True)
    university_id_proof = serializers.FileField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'dob', 'phone_number', 'address', 'university_name', 'university_id_proof']

    def create(self, validated_data):
        # Extract related fields for the Student profile
        dob = validated_data.pop('dob')
        phone_number = validated_data.pop('phone_number')
        address = validated_data.pop('address')
        university_name = validated_data.pop('university_name')
        university_id_proof = validated_data.pop('university_id_proof')

        # Create User object
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        # Add user to "Students" group
        add_user_to_student_group(user)

        # Create Student profile linked to the User
        student = Student.objects.create(
            user=user,
            dob=dob,
            phone_number=phone_number,
            address=address,
            university_name=university_name,
            university_id_proof=university_id_proof
        )
        student.full_clean()
        student.save()
        return user
    
    def validate_phone_number(self, value):
        # Check if the phone number is in the format +1 followed by 10 to 12 digits or just 10 to 12 digits without +1
        if not re.fullmatch(r'(\+1)?\d{10,12}$', value):
            raise serializers.ValidationError("Phone number must be in the format +1 followed by 10 to 12 digits, or just 10 to 12 digits.")
        return value
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Student
        fields = '__all__'

    def validate_phone_number(self, value):
        # Ensure the phone number follows the required format.
        phone_digits = value.replace('+', '').replace(' ', '').replace('-', '')
        if len(phone_digits) not in [10, 11] or (len(phone_digits) == 11 and not phone_digits.startswith('1')):
            raise serializers.ValidationError("Phone number must have exactly 10 digits or start with '+1'.")
        return value
