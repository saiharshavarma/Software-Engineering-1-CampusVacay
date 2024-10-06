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