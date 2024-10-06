<<<<<<< HEAD
from rest_framework import serializers
from .models import Student
from django.contrib.auth.models import User

class StudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', max_length=150)
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = Student
        fields = ['username', 'email', 'dob', 'phone_number', 'address', 'university_name', 'university_id_proof']

    # Validation for username
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    # Validation for email
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value
    
    def validate_phone_number(self, value):
        if value:
            value = value.replace('+', '').replace(' ', '').replace('-', '')
            
            if len(value) == 10:
                value = '+1' + value
            elif len(value) == 11 and value.startswith('1'):
                value = '+' + value
            else:
                raise serializers.ValidationError("Phone number must have exactly 10 digits or start with '+1' followed by 10 digits.")
        return value
=======
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Student, add_user_to_student_group

class UserRegistrationSerializer(serializers.ModelSerializer):
    dob = serializers.DateField(write_only=True, input_formats=['%Y-%m-%d', '%m/%d/%Y', '%d-%m-%Y'] )
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
>>>>>>> api
