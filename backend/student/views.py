from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Student
from .forms import StudentRegistrationForm, StudentLoginForm
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
            student.full_clean()
            student.save()
            # Log in the user after registration
            login(request, user)
            messages.success(request, "Registration successful!")
            return render(request, 'student_registration.html', {'form': form})  # Redirect to a 'home' page after successful registration

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