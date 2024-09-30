from django.contrib.auth.context_processors import auth
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import HotelRegistrationForm, HotelLoginForm
from .models import add_user_to_hotel_group
from .models import Hotel, RoomsDescription, CustomerReviews
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required


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