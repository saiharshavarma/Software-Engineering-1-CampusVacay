from django.contrib.auth.context_processors import auth
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import HotelRegistrationForm, HotelLoginForm
from .models import add_user_to_hotel_group
from .models import Hotel, RoomsDescription, CustomerReviews, Reservation
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer, ReservationSerializer, ReservationListSerializer, ReservationDetailSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import generics, status
from .serializers import HotelSerializer
from rest_framework.generics import ListAPIView, UpdateAPIView
from django.db.models import Q
from datetime import datetime

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token = request.user.auth_token
            return Response({"message": "Successfully logged out."})
        except:
            return Response({"error": "Something went wrong."}, status=400)

@login_required
def hotel_dashboard(request):
    # Get the logged-in user's hotel profile
    hotel = get_object_or_404(Hotel, user=request.user)

    # Fetch the rooms associated with this hotel
    rooms = RoomsDescription.objects.filter(hotel=hotel)

    # Fetch the reviews for this hotel
    reviews = CustomerReviews.objects.filter(hotel=hotel)

    context = {
        'hotel': hotel,
        'rooms': rooms,
        'reviews': reviews
    }
    return render(request, 'hotel_dashboard.html', context)


class HotelDashboardView(ListAPIView):
    serializer_class = ReservationDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the selected date from query parameters (default to today)
        date_str = self.request.query_params.get('date', datetime.today().strftime('%Y-%m-%d'))
        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        # Filter reservations for this hotel on the selected date
        return Reservation.objects.filter(
            room__hotel__user=self.request.user, 
            check_in_date=date
        ).order_by('check_in_date')

class UpdateReservationView(UpdateAPIView):
    serializer_class = ReservationDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ensure that only the hotel manager can update their hotel’s reservations
        return Reservation.objects.filter(room__hotel__user=self.request.user)

class HotelSearchView(APIView):
    def post(self, request):
        # Extract parameters from request body
        destination = request.data.get('destination')
        check_in_date = request.data.get('check_in_date')
        check_out_date = request.data.get('check_out_date')
        guests = request.data.get('guests')

        # Validate input
        if not destination or not check_in_date or not check_out_date or not guests:
            return Response({"error": "All fields (destination, check_in_date, check_out_date, guests) are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        # Filter hotels by destination (city or country or location or address or hotel name)
        queryset = Hotel.objects.filter(
            Q(city__icontains=destination) | Q(country__icontains=destination) | Q(location__icontains=destination) | Q(address__icontains=destination) | Q(hotel_name__icontains=destination)
        )

        # Filter by room capacity (guests)
        queryset = queryset.filter(rooms__max_occupancy__gte=guests)

        available_hotels = {}

        for hotel in queryset:
            hotel_rooms = hotel.rooms.all()

            # Initialize an empty list of available rooms for this hotel
            available_rooms = []

            for room in hotel_rooms:
                # Count how many rooms of this type are already booked for the given date range
                booked_rooms = Reservation.objects.filter(
                    room=room,
                    check_in_date__lte=check_out_date,
                    check_out_date__gte=check_in_date
                ).count()

                # Calculate available rooms
                available_room_count = room.number_of_rooms - booked_rooms

                if available_room_count > 0:
                    room_data = {
                        "room_type": room.room_type,
                        "available_rooms": available_room_count,
                        "price_per_night": room.price_per_night,
                        "facilities": room.facilities,
                        "max_occupancy": room.max_occupancy
                    }
                    available_rooms.append(room_data)

            # Only add the hotel if there are available rooms
            if available_rooms:
                if hotel.hotel_name not in available_hotels:
                    available_hotels[hotel.hotel_name] = {
                        "hotel_id": hotel.id,
                        "hotel_name": hotel.hotel_name,
                        "address": hotel.address,
                        "description": hotel.description,
                        "facilities": hotel.facilities,
                        "check_in_time": hotel.check_in_time,
                        "check_out_time": hotel.check_out_time,
                        "rooms": available_rooms
                    }

        # Convert available_hotels to a list to return the response
        return Response(list(available_hotels.values()), status=status.HTTP_200_OK)

class RoomBookingView(APIView):
    permission_classes = [IsAuthenticated]  # Only logged-in students can book rooms

    def post(self, request, hotel_id, room_id):
        try:
            room = RoomsDescription.objects.get(id=room_id, hotel__id=hotel_id)
        except RoomsDescription.DoesNotExist:
            return Response({"error": "Room not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(student=request.user.student_profile, room=room)
            return Response({"message": "Room booked successfully!", "data": serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HotelManagerReservations(ListAPIView):
    serializer_class = ReservationListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter reservations for rooms managed by the logged-in hotel manager
        return Reservation.objects.filter(room__hotel__user=self.request.user)

def hotel_registration(request):
    if request.method == 'POST':
        form = HotelRegistrationForm(request.POST)

        if form.is_valid():
            # Create the User object (authentication details)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            hotel_name = form.cleaned_data['hotel_name']
            phone_number = form.cleaned_data['phone_number']
            address = form.cleaned_data['address']
            location = form.cleaned_data['location']
            city = form.cleaned_data['city']
            country = form.cleaned_data['country']
            hotel_photos = form.cleaned_data['hotel_photos']
            description = form.cleaned_data['description']
            facilities = form.cleaned_data['facilities']
            check_in_time = form.cleaned_data['check_in_time']
            check_out_time = form.cleaned_data['check_out_time']
            cancellation_policy = form.cleaned_data['cancellation_policy']
            student_discount = form.cleaned_data['student_discount']
            special_offers = form.cleaned_data['special_offers']

            # Check if the username or email already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
                return render(request, 'hotel_registration.html', {'form': form})

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")
                return render(request, 'hotel_registration.html', {'form': form})

            # Create the User object for the hotel
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # Add user to the "Hotels" group
            add_user_to_hotel_group(user)

            # Now handle hotel-specific details (Hotel profile creation)
            hotel = Hotel.objects.create(
                user=user,  # Associate the user with the hotel
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

            # Log in the hotel user after registration
            login(request, user)
            messages.success(request, "Hotel registered successfully!")
            return redirect('hotel_dashboard')  # Redirect to the hotel dashboard after successful registration

    else:
        form = HotelRegistrationForm()

    return render(request, 'hotel_registration.html', {'form': form})

class CancelReservationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            reservation = Reservation.objects.get(pk=pk, student=request.user.student_profile)
        except Reservation.DoesNotExist:
            return Response({"error": "Reservation not found or not authorized."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the reservation is already canceled
        if reservation.canceled:
            return Response({"error": "This reservation is already canceled."}, status=status.HTTP_400_BAD_REQUEST)

        # Cancel the reservation and save the reason (if provided)
        reason = request.data.get("cancellation_reason", "No reason provided.")
        reservation.cancel(reason)

        return Response({"message": "Reservation canceled successfully."}, status=status.HTTP_200_OK)

def view_room_details(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    rooms = RoomsDescription.objects.filter(hotel=hotel)
    return render(request, 'view_rooms.html', {'hotel': hotel, 'rooms': rooms})


def enter_new_room(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)

    if request.method == 'POST':
        room_type = request.POST.get('room_type')
        number_of_rooms = request.POST.get('number_of_rooms')
        price_per_night = request.POST.get('price_per_night')
        facilities = request.POST.get('facilities')
        breakfast_included = request.POST.get('breakfast_included') == 'true'
        room_size = request.POST.get('room_size')
        max_occupancy = request.POST.get('max_occupancy')
        smoking_allowed = request.POST.get('smoking_allowed') == 'true'

        RoomsDescription.objects.create(
            hotel=hotel,
            room_type=room_type,
            number_of_rooms=number_of_rooms,
            price_per_night=price_per_night,
            facilities=facilities,
            breakfast_included=breakfast_included,
            room_size=room_size,
            max_occupancy=max_occupancy,
            smoking_allowed=smoking_allowed
        )

        messages.success(request, "Room details added successfully!")
        return redirect('hotel_dashboard')

    return render(request, 'add_room.html', {'hotel': hotel})


def update_room(request, room_id):
    room = get_object_or_404(RoomsDescription, id=room_id)

    if request.method == 'POST':
        room.room_type = request.POST.get('room_type')
        room.number_of_rooms = request.POST.get('number_of_rooms')
        room.price_per_night = request.POST.get('price_per_night')
        room.facilities = request.POST.get('facilities')
        room.breakfast_included = request.POST.get('breakfast_included') == 'true'
        room.room_size = request.POST.get('room_size')
        room.max_occupancy = request.POST.get('max_occupancy')
        room.smoking_allowed = request.POST.get('smoking_allowed') == 'true'

        room.save()
        messages.success(request, "Room details updated successfully!")
        return redirect('hotel_dashboard')

    return render(request, 'edit_room.html', {'room': room})


def delete_room(request, room_id):
    room = get_object_or_404(RoomsDescription, id=room_id)

    if request.method == 'POST':
        room.delete()
        messages.success(request, "Room details deleted successfully!")
        return redirect('hotel_dashboard')

    return render(request, 'delete_room.html', {'room': room})


def view_hotel_reviews(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    reviews = CustomerReviews.objects.filter(hotel=hotel)
    return render(request, 'view_reviews.html', {'hotel': hotel, 'reviews': reviews})


def create_review(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    student = request.user.student_profile

    if request.method == 'POST':
        rating = request.POST.get('rating')
        review_text = request.POST.get('review')

        CustomerReviews.objects.create(
            hotel=hotel,
            student=student,
            rating=rating,
            review=review_text
        )

        messages.success(request, "Review added successfully!")
        return redirect('hotel_details', hotel_id=hotel_id)

    return render(request, 'add_review.html', {'hotel': hotel})


def edit_review(request, review_id):
    review = get_object_or_404(CustomerReviews, id=review_id)
    if request.user.student_profile != review.student:
        raise PermissionDenied()

    if request.method == 'POST':
        review.rating = request.POST.get('rating')
        review.review = request.POST.get('review')
        review.save()

        messages.success(request, "Review updated successfully!")
        return redirect('hotel_details', hotel_id=review.hotel.id)

    return render(request, 'edit_review.html', {'review': review})


def delete_review(request, review_id):
    review = get_object_or_404(CustomerReviews, id=review_id)
    if request.user.student_profile != review.student:
        raise PermissionDenied()

    if request.method == 'POST':
        review.delete()
        messages.success(request, "Review deleted successfully!")
        return redirect('hotel_details', hotel_id=review.hotel.id)

    return render(request, 'delete_review.html', {'review': review})


def hotel_login(request):
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
        # Create an instance of the HotelLoginForm
        form = HotelLoginForm(request.POST)
        # Render the hotel login page with the form
        return render(request, 'hotel_login.html', {'form': form})

    # Check if the request method is POST
    elif request.method == 'POST':
        # Create an instance of the HotelLoginForm with the POST data
        form = HotelLoginForm(request.POST)

        # Validate the form
        if form.is_valid():
            # Get the username and password from the cleaned data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Authenticate the user
            user = authenticate(username=username, password=password)
            # Check if the user is authenticated and belongs to the 'Hotels' group
            if user and user.groups.filter(name='Hotels').exists():
                # Log the user in and redirect to the hotel dashboard
                login(request, user)
                return redirect('hotel_dashboard')
            else:
                # Display an error message if the username or password is invalid
                messages.error(request, "Invalid username or password!")
                return redirect('hotel_login')
    else:
        # Create an instance of the HotelLoginForm
        form = HotelLoginForm()
        # Render the hotel login page with the form
        return render(request, 'hotel_login.html', {'form': form})


def hotel_logout(request):
    logout(request)
    return redirect('hotel_login')