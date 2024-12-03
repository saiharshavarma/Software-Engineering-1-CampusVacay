from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .models import Hotel, RoomsDescription, Reservation, CustomerReviews
from student.models import Student
from django.utils import timezone
from datetime import datetime, date, timedelta
from rest_framework.exceptions import ValidationError
from .serializers import UserRegistrationSerializer, RoomSerializer, HotelSerializer, ReservationSerializer, ReservationListSerializer, ReservationDetailSerializer
from rest_framework.test import APIClient
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile


class HotelModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='testpass', email='user@example.com')
        hotel_group, _ = Group.objects.get_or_create(name='Hotels')
        cls.user.groups.add(hotel_group)

        cls.hotel = Hotel.objects.create(
            user=cls.user,
            hotel_name="Test Hotel",
            address1="123 Test St.",
            address2="Test Location",
            city="Test City",
            country="Test Country",
            zip=11220,
            phone_number="+11234567890",
            description="Test description",
            facilities="Wi-Fi, Pool, Parking",
            check_in_time="15:00",
            check_out_time="11:00",
            cancellation_policy="No cancellation allowed after booking.",
            student_discount=10.00,
            special_offers="10% discount on weekends",
            average_rating=4.5
        )

    def test_hotel_creation(self):
        self.assertEqual(self.hotel.user, self.user)
        self.assertEqual(self.hotel.hotel_name, "Test Hotel")
        self.assertEqual(self.hotel.phone_number, "+11234567890")
        self.assertEqual(self.hotel.average_rating, 4.5)

    def test_phone_number_validation(self):
        hotel = Hotel(
            user=self.user,
            hotel_name="Invalid Phone Hotel",
            phone_number="123456"
        )
        with self.assertRaises(Exception):
            hotel.full_clean()


class RoomsDescriptionModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='hoteluser', password='password123')
        cls.hotel = Hotel.objects.create(
            user=cls.user,
            hotel_name="Test Hotel",
            city="Test City",
            phone_number="+11234567890"
        )
        cls.room = RoomsDescription.objects.create(
            hotel=cls.hotel,
            room_type="Single",
            number_of_rooms=10,
            price_per_night=100.00,
            facilities="Wi-Fi, TV, Air Conditioning",
            breakfast_included=True,
            room_size="25 sqm",
            max_occupancy=2,
            smoking_allowed=False
        )

    def test_room_creation(self):
        self.assertEqual(self.room.hotel, self.hotel)
        self.assertEqual(self.room.room_type, "Single")
        self.assertEqual(self.room.number_of_rooms, 10)
        self.assertEqual(self.room.price_per_night, 100.00)
        self.assertTrue(self.room.breakfast_included)
        self.assertEqual(self.room.max_occupancy, 2)



class ReservationModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.hotel_user = User.objects.create_user(username='hoteluser', password='password123')
        cls.student_user = User.objects.create_user(username='studentuser', password='password123')
        cls.student = Student.objects.create(
            user=cls.student_user,
            dob=date(2000, 1, 1),
            phone_number="+11234567890",
            address="456 Student Lane",
            university_name="Test University",
            date_joined=timezone.now()
        )

        cls.hotel = Hotel.objects.create(
            user=cls.hotel_user,
            hotel_name="Test Hotel",
            city="Test City",
            phone_number="+11234567890"
        )
        cls.room = RoomsDescription.objects.create(
            hotel=cls.hotel,
            room_type="Single",
            number_of_rooms=5,
            price_per_night=120.00,
            facilities="Wi-Fi, TV, Air Conditioning",
            breakfast_included=True,
            max_occupancy=2
        )

        cls.reservation = Reservation.objects.create(
            hotel=cls.hotel,
            room=cls.room,
            student=cls.student,
            first_name="John",
            last_name="Doe",
            email="johndoe@example.com",
            country="Testland",
            phone_number="+123456789",
            expected_arrival_time="15:00",
            special_requests="Near window",
            payment_mode="card",
            check_in_date=date.today(),
            check_out_date=date.today() + timedelta(days=2),
            guests=1
        )

    def test_reservation_creation(self):
        self.assertEqual(self.reservation.hotel, self.hotel)
        self.assertEqual(self.reservation.room, self.room)
        self.assertEqual(self.reservation.student, self.student)
        self.assertEqual(self.reservation.first_name, "John")
        self.assertEqual(self.reservation.last_name, "Doe")
        self.assertEqual(self.reservation.email, "johndoe@example.com")
        self.assertEqual(self.reservation.country, "Testland")
        self.assertEqual(self.reservation.phone_number, "+123456789")
        self.assertEqual(self.reservation.payment_mode, "card")
        self.assertEqual(self.reservation.check_in_date, date.today())
        self.assertEqual(self.reservation.check_out_date, date.today() + timedelta(days=2))
        self.assertEqual(self.reservation.guests, 1)
        self.assertFalse(self.reservation.canceled)

    def test_check_out_after_check_in(self):
        self.reservation.check_out_date = self.reservation.check_in_date - timedelta(days=1)
        with self.assertRaises(Exception):
            self.reservation.full_clean()

    def test_cancel_reservation(self):
        reason = "Change of plans"
        self.reservation.cancel(reason=reason)
        self.assertTrue(self.reservation.canceled)
        self.assertEqual(self.reservation.cancellation_reason, reason)
        self.assertIsNotNone(self.reservation.cancellation_date)


class CustomerReviewsModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.hotel_user = User.objects.create_user(username='hoteluser', password='password123')
        cls.hotel = Hotel.objects.create(
            user=cls.hotel_user,
            hotel_name="Test Hotel",
            city="Test City",
            phone_number="+11234567890"
        )

        cls.student_user = User.objects.create_user(username='studentuser', password='password123')
        cls.student = Student.objects.create(
            user=cls.student_user,
            dob=date(2000, 1, 1),
            phone_number="+11234567890",
            address="456 Student Lane",
            university_name="Test University",
            date_joined=timezone.now()
        )

        cls.review = CustomerReviews.objects.create(
            hotel=cls.hotel,
            student=cls.student,
            rating=4,
            review="Great experience!",
            date_added=timezone.now()
        )

    def test_review_creation(self):
        self.assertEqual(self.review.hotel, self.hotel)
        self.assertEqual(self.review.student, self.student)
        self.assertEqual(self.review.rating, 4)
        self.assertEqual(self.review.review, "Great experience!")
        self.assertIsNotNone(self.review.date_added)

        self.review.rating = 3 
        try:
            self.review.full_clean()
        except Exception:
            self.fail("Review with valid rating raised unexpected exception.")

    def test_string_representation(self):
        expected_str = f'Review by {self.student.user.username} for {self.hotel.hotel_name} - 4 stars on {self.review.date_added}'
        self.assertEqual(str(self.review), expected_str)


class UserRegistrationSerializerTest(TestCase):

    def setUp(self):
        self.user_data = {
            "username": "testhotel",
            "password": "securepassword",
            "email": "testhotel@example.com",
            "hotel_name": "Test Hotel",
            "phone_number": "+11234567890",
            "address1": "123 Test St.",
            "address2": "Test Location",
            "city": "Test City",
            "country": "Test Country",
            "zip": 11220,
            "hotel_photos": SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg"),
            "description": "A cozy place",
            "facilities": "Wi-Fi, Parking, Pool",
            "check_in_time": "15:00",
            "check_out_time": "11:00",
            "cancellation_policy": "Non-refundable",
            "student_discount": 5.00,
            "special_offers": "10% off on weekends"
        }

    def test_user_registration_serializer_valid(self):
        serializer = UserRegistrationSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, "testhotel")
        self.assertEqual(user.email, "testhotel@example.com")
        self.assertEqual(user.hotel_profile.hotel_name, "Test Hotel")

    def test_user_registration_serializer_invalid_phone(self):
        self.user_data["phone_number"] = "123ABC"
        serializer = UserRegistrationSerializer(data=self.user_data)
        is_valid = serializer.is_valid()
        self.assertFalse(is_valid, "Serializer should be invalid for incorrect phone number format.")
        self.assertIn("phone_number", serializer.errors)


class RoomSerializerTest(TestCase):

    def setUp(self):
        self.hotel_user = User.objects.create_user(username="hoteluser", password="password123")
        self.hotel = Hotel.objects.create(
            user=self.hotel_user,
            hotel_name="Test Hotel",
            city="Test City",
            phone_number="+11234567890"
        )
        self.room_data = {
            "hotel": self.hotel.id,
            "room_type": "Deluxe Suite",
            "number_of_rooms": 5,
            "price_per_night": 200.00,
            "facilities": "Wi-Fi, Mini-bar, Sea View",
            "breakfast_included": True,
            "room_size": "50 sqm",
            "max_occupancy": 3,
            "smoking_allowed": False
        }

    def test_room_serializer_valid(self):
        serializer = RoomSerializer(data=self.room_data)
        self.assertTrue(serializer.is_valid())
        room = serializer.save()
        self.assertEqual(room.room_type, "Deluxe Suite")
        self.assertEqual(room.price_per_night, 200.00)
        self.assertTrue(room.breakfast_included)


class HotelSerializerTest(TestCase):

    def setUp(self):
        self.hotel_user = User.objects.create_user(username="hoteluser", password="password123")
        self.hotel = Hotel.objects.create(
            user=self.hotel_user,
            hotel_name="Test Hotel",
            city="Test City",
            phone_number="+11234567890",
            facilities="Wi-Fi, Pool",
            description="A lovely place to stay"
        )
        RoomsDescription.objects.create(
            hotel=self.hotel,
            room_type="Single",
            number_of_rooms=5,
            price_per_night=120.00,
            facilities="Wi-Fi, Air Conditioning",
            max_occupancy=2
        )

    def test_hotel_serializer_fields(self):
        serializer = HotelSerializer(instance=self.hotel)
        data = serializer.data
        self.assertEqual(data["hotel_name"], "Test Hotel")
        self.assertEqual(data["facilities"], "Wi-Fi, Pool")
        self.assertEqual(len(data["rooms"]), 1)


class ReservationSerializerTest(TestCase):

    def setUp(self):
        self.hotel_user = User.objects.create_user(username="hoteluser", password="password123")
        self.student_user = User.objects.create_user(username="studentuser", password="password123")
        self.student = Student.objects.create(
            user=self.student_user,
            dob=date(2000, 1, 1),
            phone_number="+11234567890",
            university_name="Test University"
        )
        self.hotel = Hotel.objects.create(
            user=self.hotel_user,
            hotel_name="Test Hotel",
            city="Test City",
            phone_number="+11234567890"
        )
        self.room = RoomsDescription.objects.create(
            hotel=self.hotel,
            room_type="Single",
            number_of_rooms=5,
            price_per_night=100.00
        )
        self.reservation_data = {
            "hotel": self.hotel.id,
            "room": self.room.id,
            "student": self.student.id,
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "country": "Testland",
            "phone_number": "+123456789",
            "expected_arrival_time": "15:00",
            "special_requests": "Near window",
            "payment_mode": "card",
            "check_in_date": date.today(),
            "check_out_date": date.today() + timedelta(days=2),
            "guests": 1
        }

    def test_reservation_serializer_valid(self):
        serializer = ReservationSerializer(data=self.reservation_data)
        self.assertTrue(serializer.is_valid())
        reservation = serializer.save()
        self.assertEqual(reservation.hotel, self.hotel)
        self.assertEqual(reservation.room, self.room)
        self.assertEqual(reservation.student, self.student)
        self.assertEqual(reservation.first_name, "John")

    def test_reservation_serializer_invalid_dates(self):
        self.reservation_data["check_out_date"] = self.reservation_data["check_in_date"] - timedelta(days=1)
        serializer = ReservationSerializer(data=self.reservation_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)


class ReservationListSerializerTest(TestCase):

    def setUp(self):
        self.hotel_user = User.objects.create_user(username="hoteluser", password="password123")
        self.student_user = User.objects.create_user(username="studentuser", password="password123")
        self.student = Student.objects.create(user=self.student_user, dob=date(2000, 1, 1), university_name="Test University")
        self.hotel = Hotel.objects.create(user=self.hotel_user, hotel_name="Test Hotel", city="Test City", phone_number="+11234567890")
        self.room = RoomsDescription.objects.create(hotel=self.hotel, room_type="Single", number_of_rooms=5, price_per_night=100.00)
        self.reservation = Reservation.objects.create(
            hotel=self.hotel,
            room=self.room,
            student=self.student,
            first_name="John",
            last_name="Doe",
            email="johndoe@example.com",
            country="Testland",
            phone_number="+123456789",
            check_in_date=date.today(),
            check_out_date=date.today() + timedelta(days=2),
            guests=1
        )

    def test_reservation_list_serializer_fields(self):
        serializer = ReservationListSerializer(instance=self.reservation)
        data = serializer.data
        self.assertEqual(data["hotel_name"], "Test Hotel")
        self.assertEqual(data["room_type"], "Single")
        self.assertEqual(data["first_name"], "John")
        self.assertEqual(data["check_in_date"], date.today().isoformat())
        self.assertEqual(data["check_out_date"], (date.today() + timedelta(days=2)).isoformat())

class UserRegistrationViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "username": "testhotel",
            "password": "securepassword",
            "email": "testhotel@example.com",
            "hotel_name": "Test Hotel",
            "phone_number": "+11234567890",
            "address1": "123 Test St.",
            "address2": "Test Location",
            "city": "Test City",
            "country": "Test Country",
            "zip": 11220,
            "hotel_photos": SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg"),  # Mock file
            "description": "A cozy place",
            "facilities": "Wi-Fi, Parking, Pool",
            "check_in_time": "15:00",
            "check_out_time": "11:00",
            "cancellation_policy": "Non-refundable",
            "student_discount": 5.00,
            "special_offers": "10% off on weekends"
        }
        self.url = reverse('user-register')

    def test_user_registration_success(self):
        response = self.client.post(self.url, self.user_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("username", response.data)
        self.assertEqual(response.data["username"], "testhotel")


class LoginLogoutViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.login_url = reverse('api_login')
        self.logout_url = reverse('api_logout')

    def test_login_success(self):
        response = self.client.post(self.login_url, {"username": "testuser", "password": "testpass"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_login_failure(self):
        response = self.client.post(self.login_url, {"username": "testuser", "password": "wrongpass"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

    def test_logout(self):
        login_response = self.client.post(self.login_url, {"username": "testuser", "password": "testpass"})
        token = login_response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)


class HotelDashboardViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        
        self.user = User.objects.create_user(username="hoteluser", password="password123")
        self.hotel = Hotel.objects.create(user=self.user, hotel_name="Test Hotel", city="Test City", phone_number="+11234567890")
        
        self.student_user = User.objects.create_user(username="studentuser", password="password123")
        self.student = Student.objects.create(
            user=self.student_user,
            dob=date(2000, 1, 1),
            phone_number="+11234567890",
            university_name="Test University"
        )
        
        self.room = RoomsDescription.objects.create(
            hotel=self.hotel,
            room_type="Single",
            number_of_rooms=5,
            price_per_night=120.00,
            max_occupancy=2
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

        self.client.force_authenticate(user=self.user)
        self.url = reverse('hotel-dashboard')

    def test_dashboard_access(self):
        response = self.client.get(self.url, {'date': date.today().strftime('%Y-%m-%d')})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 1)
        reservation_data = response.data[0]
        
        self.assertEqual(reservation_data["first_name"], "John")
        self.assertEqual(reservation_data["last_name"], "Doe")
        self.assertEqual(reservation_data["email"], "johndoe@example.com")
        self.assertEqual(reservation_data["check_in_date"], date.today().isoformat())


class HotelSearchViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="hoteluser", password="password123")
        self.hotel = Hotel.objects.create(
            user=self.user,
            hotel_name="Test Hotel",
            city="Test City",
            phone_number="+11234567890",
            facilities="Wi-Fi, Pool",
            description="A lovely place to stay"
        )
        self.room = RoomsDescription.objects.create(
            hotel=self.hotel,
            room_type="Single",
            number_of_rooms=5,
            price_per_night=120.00,
            facilities="Wi-Fi, TV",
            max_occupancy=2
        )
        self.search_url = reverse('hotel-search')

    def test_hotel_search_success(self):
        response = self.client.post(self.search_url, {
            "location": "Test City",
            "check_in": date.today().isoformat(),
            "check_out": (date.today() + timedelta(days=1)).isoformat(),
            "guests": 1
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("hotel_name", response.data[0])
        self.assertEqual(response.data[0]["hotel_name"], "Test Hotel")

    def test_hotel_search_missing_fields(self):
        response = self.client.post(self.search_url, {
            "location": "Test City",
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)


class RoomBookingViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        
        self.hotel_user = User.objects.create_user(username="hoteluser", password="password123")
        self.student_user = User.objects.create_user(username="studentuser", password="password123")
        
        self.student = Student.objects.create(
            user=self.student_user,
            dob=date(2000, 1, 1),
            phone_number="+11234567890",
            university_name="Test University"
        )
        
        self.hotel = Hotel.objects.create(
            user=self.hotel_user, 
            hotel_name="Test Hotel", 
            city="Test City", 
            phone_number="+11234567890"
        )
        self.room = RoomsDescription.objects.create(
            hotel=self.hotel, 
            room_type="Single", 
            number_of_rooms=5, 
            price_per_night=100.00
        )
        
        self.client.force_authenticate(user=self.student_user)
        
        self.booking_url = reverse('book-room', args=[self.hotel.id, self.room.id])

    def test_room_booking_success(self):
        response = self.client.post(self.booking_url, {
            "hotel": self.hotel.id,
            "room": self.room.id,
            "student": self.student.id,
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "country": "Testland",
            "phone_number": "+123456789",
            "expected_arrival_time": "15:00",
            "check_in_date": date.today().isoformat(),
            "check_out_date": (date.today() + timedelta(days=2)).isoformat(),
            "guests": 1
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)
        self.assertEqual(response.data["message"], "Room booked successfully!")

    def test_room_booking_invalid_dates(self):
        response = self.client.post(self.booking_url, {
            "hotel": self.hotel.id,
            "room": self.room.id,
            "student": self.student.id,
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "country": "Testland",
            "phone_number": "+123456789",
            "expected_arrival_time": "15:00",
            "check_in_date": date.today().isoformat(),
            "check_out_date": (date.today() - timedelta(days=1)).isoformat(),
            "guests": 1
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)