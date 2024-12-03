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
from .serializers import UserRegistrationSerializer, StudentProfileSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from hotel.models import Reservation
from hotel.serializers import HotelSerializer, ReservationListSerializer
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
# from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import status
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
    """
    APIView for viewing and editing the student's profile.
    """
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only allow access to the Student profile for the logged-in user
        return Student.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
            """
            Retrieve the authenticated user's hotel profile.
            """
            # Fetch the hotel profile associated with the logged-in user
            student = get_object_or_404(Student, user=request.user)
            serializer = self.serializer_class(student)
            # Serialize the hotel profile
            #serializer = StudentProfileSerializer(student)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        """
        Partially update the student profile, including related User fields.
        """
        student_profile = self.get_queryset().first()  # Get the logged-in user's profile
        user = student_profile.user  # Access the related User object

        # Separate User-related data and Student-related data
        user_fields = ['username', 'email', 'first_name', 'last_name']  # Add all fields from the User model you want to update
        user_data = {key: request.data[key] for key in user_fields if key in request.data}
        student_data = {key: request.data[key] for key in request.data if key not in user_fields}

        # Update the User model fields
        if user_data:
            user_serializer = UserSerializer(user, data=user_data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()
            else:
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Update the Student model fields
        if student_data:
            serializer = self.get_serializer(student_profile, data=student_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "No valid fields provided for update."}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        """
        Fully update the student profile, including related User fields.
        """
        student_profile = self.get_queryset().first()  # Get the logged-in user's profile
        user = student_profile.user  # Access the related User object

        # Separate User-related data and Student-related data
        user_fields = ['username', 'email', 'first_name', 'last_name']
        user_data = {key: request.data[key] for key in user_fields if key in request.data}
        student_data = {key: request.data[key] for key in request.data if key not in user_fields}

        # Update the User model fields
        if user_data:
            user_serializer = UserSerializer(user, data=user_data)
            if user_serializer.is_valid():
                user_serializer.save()
            else:
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Update the Student model fields
        if student_data:
            serializer = self.get_serializer(student_profile, data=student_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "No valid fields provided for update."}, status=status.HTTP_400_BAD_REQUEST)

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

class AddFavoriteHotelView(ViewSet):
    """
    ViewSet for students to add hotels to their favorite list.
    """
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Add a hotel to the student's list of favorites.
        """
        hotel_id = request.data.get('hotel_id')
        if not hotel_id:
            return Response({"error": "Hotel ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Get the logged-in student's profile
        student = get_object_or_404(Student, user=request.user)

        # Get the hotel instance
        hotel = get_object_or_404(Hotel, id=hotel_id)

        # Add hotel to student's favorites
        if hotel in student.favorite_hotels.all():
            return Response({"message": "This hotel is already in your list of favorite hotels."}, status=status.HTTP_200_OK)

        student.favorite_hotels.add(hotel)
        return Response({"message": f"Hotel '{hotel.hotel_name}' added to favorites."}, status=status.HTTP_200_OK)
    
    def list(self, request, *args, **kwargs):
        """
        Retrieve the list of favorite hotels for the logged-in student.
        """
        student = get_object_or_404(Student, user=request.user)
        favorite_hotels = student.favorite_hotels.all()
        serializer = HotelSerializer(favorite_hotels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk=None, *args, **kwargs):
        """
        Remove a hotel from the student's list of favorites.
        """
        student = get_object_or_404(Student, user=request.user)
        hotel = get_object_or_404(Hotel, id=pk)

        if hotel not in student.favorite_hotels.all():
            return Response({"error": "This hotel is not in your list of favorite hotels."}, status=status.HTTP_400_BAD_REQUEST)

        student.favorite_hotels.remove(hotel)
        return Response({"message": f"Hotel '{hotel.hotel_name}' removed from favorites."}, status=status.HTTP_200_OK)