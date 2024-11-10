from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Student
from hotel.models import Reservation, Hotel, RoomsDescription, CustomerReviews
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from .serializers import UserRegistrationSerializer, StudentProfileSerializer


class StudentModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="studentuser", password="password123")

    def test_create_student(self):
        student = Student.objects.create(
            user=self.user,
            dob=date(2000, 1, 1),
            phone_number="+11234567890",
            address="123 Main St",
            university_name="Test University",
            university_id_proof=SimpleUploadedFile("test_id.pdf", b"file_content", content_type="application/pdf")
        )
        self.assertEqual(student.user.username, "studentuser")
        self.assertEqual(student.phone_number, "+11234567890")
        self.assertEqual(student.university_name, "Test University")

    def test_invalid_phone_number(self):
        student = Student(
            user=self.user,
            dob=date(2000, 1, 1),
            phone_number="12345",
            address="123 Main St",
            university_name="Test University"
        )
        with self.assertRaises(ValidationError):
            student.full_clean()

    def test_string_representation(self):
        student = Student.objects.create(
            user=self.user,
            dob=date(2000, 1, 1),
            phone_number="+11234567890",
            address="123 Main St",
            university_name="Test University"
        )
        self.assertEqual(str(student), "studentuser - Student Profile")


class UserRegistrationSerializerTest(TestCase):

    def setUp(self):
        self.user_data = {
            "username": "teststudent",
            "password": "testpassword",
            "first_name": "John",
            "last_name": "Doe",
            "email": "teststudent@example.com",
            "dob": "2000-01-01",
            "phone_number": "+11234567890",
            "address": "123 Main St",
            "university_name": "Test University",
            "university_id_proof": SimpleUploadedFile("test_id.pdf", b"file_content", content_type="application/pdf")
        }

    def test_user_registration_serializer_valid(self):
        serializer = UserRegistrationSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, "teststudent")
        self.assertEqual(user.student_profile.university_name, "Test University")

    def test_user_registration_serializer_invalid_phone(self):
        self.user_data["phone_number"] = "12345"
        serializer = UserRegistrationSerializer(data=self.user_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("phone_number", serializer.errors)


class StudentProfileSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="studentuser", password="password123")
        self.student = Student.objects.create(
            user=self.user,
            dob=date(2000, 1, 1),
            phone_number="+11234567890",
            address="123 Main St",
            university_name="Test University",
            university_id_proof=SimpleUploadedFile("test_id.pdf", b"file_content", content_type="application/pdf")
        )

    def test_student_profile_serializer_data(self):
        serializer = StudentProfileSerializer(instance=self.student)
        data = serializer.data
        self.assertEqual(data["dob"], "2000-01-01")
        self.assertEqual(data["phone_number"], "+11234567890")
        self.assertEqual(data["university_name"], "Test University")

    def test_student_profile_serializer_invalid_phone(self):
        invalid_data = {
            "dob": "2000-01-01",
            "phone_number": "12345",
            "address": "123 Main St",
            "university_name": "Test University",
            "university_id_proof": SimpleUploadedFile("test_id.pdf", b"file_content", content_type="application/pdf")
        }
        serializer = StudentProfileSerializer(instance=self.student, data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("phone_number", serializer.errors)


class UserRegistrationViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.registration_url = reverse('student-user-register')
        self.user_data = {
            "username": "teststudent",
            "password": "testpassword",
            "email": "teststudent@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "dob": "2000-01-01",
            "phone_number": "+11234567890",
            "address": "123 Main St",
            "university_name": "Test University",
            "university_id_proof": SimpleUploadedFile("test_id.pdf", b"file_content", content_type="application/pdf")
        }

    def test_user_registration_success(self):
        response = self.client.post(self.registration_url, self.user_data, format="multipart")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)
        self.assertEqual(response.data["message"], "User registered successfully!")
        self.assertIn("data", response.data)
        self.assertEqual(response.data["data"]["username"], "teststudent")


class LogoutViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        self.logout_url = reverse('api_logout')

    def test_logout_success(self):
        response = self.client.post(self.logout_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
        self.assertEqual(response.data["message"], "Successfully logged out.")


class StudentProfileViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="studentuser", password="password123")
        self.student = Student.objects.create(
            user=self.user,
            dob=date(2000, 1, 1),
            phone_number="+11234567890",
            address="123 Test Lane",
            university_name="Test University"
        )
        self.client.force_authenticate(user=self.user)
        self.profile_url = reverse('student-profile')

    def test_retrieve_student_profile(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["dob"], "2000-01-01")

    def test_update_student_profile(self):
        updated_data = {
            "dob": "2001-02-02",
            "phone_number": "+1234567890",
            "address": "456 Updated Address",
            "university_name": "Updated University"
        }
        response = self.client.put(self.profile_url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["dob"], "2001-02-02")
        self.assertEqual(response.data["university_name"], "Updated University")


class StudentReservationHistoryTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        
        self.student_user = User.objects.create_user(username="studentuser", password="password123")
        self.student = Student.objects.create(
            user=self.student_user,
            dob=date(2000, 1, 1),
            phone_number="+11234567890",
            address="123 Main St",
            university_name="Test University"
        )
        
        self.client.force_authenticate(user=self.student_user)
        
        self.hotel = Hotel.objects.create(
            user=self.student_user,
            hotel_name="Test Hotel",
            address="123 Test St",
            location="Test Location",
            city="Test City",
            country="Test Country",
            phone_number="+11234567890",
            description="A lovely hotel",
            facilities="Wi-Fi, Pool, Gym",
            check_in_time="15:00",
            check_out_time="11:00",
            cancellation_policy="Non-refundable",
            student_discount=10.00,
            special_offers="Free breakfast on weekends"
        )
        self.room = RoomsDescription.objects.create(
            hotel=self.hotel,
            room_type="Single",
            number_of_rooms=5,
            price_per_night=120.00,
            facilities="Wi-Fi, TV, Air Conditioning",
            breakfast_included=True,
            room_size="25 sqm",
            max_occupancy=2,
            smoking_allowed=False
        )

        self.reservation = Reservation.objects.create(
            hotel=self.hotel,
            room=self.room,
            student=self.student,
            first_name="John",
            last_name="Doe",
            email="johndoe@example.com",
            country="Testland",
            phone_number="+123456789",
            expected_arrival_time="15:00",
            check_in_date=date.today(),
            check_out_date=date.today() + timedelta(days=2),
            guests=1
        )
        
        self.history_url = reverse('student-reservations')

    def test_reservation_history(self):
        response = self.client.get(self.history_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
        reservation_data = response.data[0]
        self.assertEqual(reservation_data["room_type"], "Single")
        self.assertEqual(reservation_data["first_name"], "John")
        self.assertEqual(reservation_data["email"], "johndoe@example.com")
        self.assertEqual(reservation_data["check_in_date"], date.today().isoformat())
