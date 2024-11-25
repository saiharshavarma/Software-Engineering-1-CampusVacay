from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import StudentRegistrationForm, StudentLoginForm
from .models import Student, add_user_to_student_group
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework import serializers
from .serializers import UserRegistrationSerializer, StudentProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from hotel.models import Reservation
from hotel.serializers import ReservationListSerializer
from rest_framework.permissions import IsAuthenticated
# from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
# from datetime import datetime
import requests

from hotel.models import Hotel, RoomsDescription, CustomerReviews

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny] 

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response({
            "message": "User registered successfully!",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user = serializer.save(is_active=False)
        send_email(user)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token = request.user.auth_token
            return Response({"message": "Successfully logged out."})
        except:
            return Response({"error": "Something went wrong."}, status=400)

def student_registration(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']

            # Ensure the username and email are unique
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
                return render(request, 'student_registration.html', {'form': form})

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")
                return render(request, 'student_registration.html', {'form': form})

            # Create the User and Student
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password
            )

            # Add user to "Students" group
            add_user_to_student_group(user)

            # Create the Student profile
            student = Student.objects.create(
                user=user,
                dob=form.cleaned_data['dob'],
                phone_number=form.cleaned_data['phone_number'],
                address=form.cleaned_data['address'],
                university_name=form.cleaned_data['university_name'],
                university_id_proof=form.cleaned_data['university_id_proof']
            )
            student.full_clean()
            student.save()
            # Log in the user after registration
            login(request, user)
            messages.success(request, "Registration successful!")
            return render(request, 'student_registration.html',
                          {'form': form})  # Redirect to a 'home' page after successful registration

        else:
            messages.error(request, "Please correct the errors below.")

    else:
        form = StudentRegistrationForm()

    return render(request, 'student_registration.html', {'form': form})


def student_login(request):
    # Check if the request method is GET
    if request.method == 'GET':
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Check if the user belongs to the 'Hotels' group
            if request.user.groups.filter(name='Hotels').exists():
                # Redirect to the hotel dashboard if the user is in the 'Hotels' group
                return redirect('hotel_dashboard')
            # Check if the user belongs to the 'Students' group
            elif request.user.groups.filter(name='Students').exists():
                # Render the index page if the user is in the 'Students' group
                return render(request, 'index.html')
        # Create an instance of the StudentLoginForm
        form = StudentLoginForm(request.POST)
        # Render the student login page with the form
        return render(request, 'student_login.html', {'form': form})

    # Check if the request method is POST
    elif request.method == 'POST':
        # Create an instance of the StudentLoginForm with the POST data
        form = StudentLoginForm(request.POST)

        # Validate the form
        if form.is_valid():
            # Get the username and password from the cleaned data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Authenticate the user
            user = authenticate(username=username, password=password)
            # Check if the user is authenticated and belongs to the 'Students' group
            if user and user.groups.filter(name='Students').exists():
                # Log the user in and render the index page
                login(request, user)
                return render(request, 'index.html')
            else:
                # Display an error message if the username or password is invalid
                messages.error(request, "Invalid username or password!")
                return redirect('student_login')
    else:
        # Create an instance of the StudentLoginForm
        form = StudentLoginForm()
        # Render the student login page with the form
        return render(request, 'student_login.html', {'form': form})


def student_logout(request):
    logout(request)
    return redirect('student_login')

class StudentProfileView(RetrieveUpdateAPIView):
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Ensure only the logged-in student can edit their profile
        try:
            return self.request.user.student_profile
        except Student.DoesNotExist:
            raise serializers.ValidationError("Student profile not found.")

class StudentReservationHistory(ListAPIView):
    serializer_class = ReservationListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter reservations by the logged-in student
        return Reservation.objects.filter(student=self.request.user.student_profile)

class StudentSearchView(APIView):
    def post(self, request):
        destination = request.data.get('destination')
        check_in_date = request.data.get('check_in_date')
        check_out_date = request.data.get('check_out_date')
        guests = request.data.get('guests')

        if not destination or not check_in_date or not check_out_date or not guests:
            return Response({"error": "All fields (destination, check_in_date, check_out_date, guests) are required."}, status=status.HTTP_400_BAD_REQUEST)

        search_payload = {
            "destination": destination,
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
            "guests": guests
        }
        try:
            response = requests.post('http://localhost:8000/hotel/api/search/', data=search_payload)
            if response.status_code == 200:
                return Response(response.json(), status=status.HTTP_200_OK)
            else:
                return Response(response.json(), status=response.status_code)
        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def view_room_details(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    rooms = RoomsDescription.objects.filter(hotel=hotel)
    return render(request, 'view_rooms.html', {'hotel': hotel, 'rooms': rooms})

def view_hotel_reviews(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    reviews = CustomerReviews.objects.filter(hotel=hotel)
    return render(request, 'view_reviews.html', {'hotel': hotel, 'reviews': reviews})