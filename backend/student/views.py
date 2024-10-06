from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Student
from .serializers import StudentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .models import add_user_to_student_group
from rest_framework.permissions import AllowAny

# Student Registration API
class StudentRegistration(APIView):
    def post(self, request):
        data = request.data
        serializer = StudentSerializer(data=data)
        permission_classes = [AllowAny]

        if serializer.is_valid():
            username = data['username']
            email = data['email']
            first_name = data['first_name']
            last_name = data['last_name']
            password = data['password']

            # Ensure the username and email are unique
            if User.objects.filter(username=username).exists():
                return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(email=email).exists():
                return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

            # Create the user and student
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password
            )

            # Add user to "Students" group if applicable (not shown in the uploaded models)
            add_user_to_student_group(user)

            # Create the Student profile
            student = Student.objects.create(
                user=user,
                dob=data['dob'],
                phone_number=data['phone_number'],
                address=data['address'],
                university_name=data['university_name'],
                university_id_proof=data['university_id_proof']
            )

            # Return success response
            return Response({"success": "Student registered successfully"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Student Login API
class StudentLogin(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.groups.filter(name='Students').exists():
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token": token.key, "message": "Login successful"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "User is not a student"}, status=status.HTTP_403_FORBIDDEN)
        return Response({"error": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)


# Student Logout API
class StudentLogout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)