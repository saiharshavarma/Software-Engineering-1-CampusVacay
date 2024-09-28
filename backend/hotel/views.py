from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import HotelRegistrationForm
from .models import add_user_to_hotel_group
from .models import Hotel, RoomsDescription, CustomerReviews

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
            return render(request, 'hotel_registration.html', {'form': form}) # Redirect to the hotel dashboard after successful registration

    else:
        form = HotelRegistrationForm()

    return render(request, 'hotel_registration.html', {'form': form})