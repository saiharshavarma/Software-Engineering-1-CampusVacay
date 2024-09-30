from django import forms
from django.contrib.auth.models import User
from .models import Student

class StudentRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    dob = forms.DateField(required=True, widget=forms.TextInput(attrs={'type': 'date'}))
    phone_number = forms.CharField(max_length=12, required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)
    university_name = forms.CharField(max_length=100, required=True)
    university_id_proof = forms.FileField(required=True)

    class Meta:
        model = Student
        fields = ['dob', 'phone_number', 'address', 'university_name', 'university_id_proof']

class StudentLoginForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

    class Meta:
        model = Student
        fields = []