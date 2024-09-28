from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from .models import Student
from .forms import StudentRegistrationForm
from .models import add_user_to_student_group

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

            # Log in the user after registration
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')  # Redirect to a 'home' page after successful registration

        else:
            messages.error(request, "Please correct the errors below.")

    else:
        form = StudentRegistrationForm()

    return render(request, 'student_registration.html', {'form': form})