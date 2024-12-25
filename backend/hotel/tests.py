from django.test import TestCase
from unittest.mock import patch
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .models import Hotel, RoomsDescription, Reservation, CustomerReviews
from student.models import Student
from django.utils import timezone
from datetime import datetime, date, timedelta
from rest_framework.exceptions import ValidationError
from .serializers import UserRegistrationSerializer, RoomSerializer, HotelSerializer, ReservationSerializer, ReservationListSerializer, ReservationDetailSerializer
from rest_framework.test import APIClient, APITestCase
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
            phone_number="+11234567890",
            zip = "11201"
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
            phone_number="+11234567890",
            zip = "11201"
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
            phone_number="+11234567890",
            zip="11201"
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
            "address1": "Time Square.",
            "address2": "Time Square",
            "city": "New York",
            "country": "United States",
            "zip": 11220,
            "hotel_photos": SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg"),
            "description": "A cozy place",
            "facilities": "Wi-Fi, Parking, Pool",
            "check_in_time": "15:00",
            "check_out_time": "11:00",
            "cancellation_policy": "Non-refundable",
            "student_discount": 5.00,
            "special_offers": "10% off on weekends",
            "tourist_spots": ['Museum', 'Park', 'Historic Site']
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
            phone_number="+11234567890",
            zip = "11201"
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
            description="A lovely place to stay",
            zip = "11201"
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
            university_name="Test University",
        )
        self.hotel = Hotel.objects.create(
            user=self.hotel_user,
            hotel_name="Test Hotel",
            city="Test City",
            phone_number="+11234567890",
            zip = "11201"
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
        self.hotel = Hotel.objects.create(user=self.hotel_user, hotel_name="Test Hotel", city="Test City", phone_number="+11234567890", zip="11201")
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
            "address1": "Time Square.",
            "address2": "Time Square",
            "city": "New York",
            "country": "United States",
            "zip": 11220,
            "hotel_photos": SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg"),  # Mock file
            "description": "A cozy place",
            "facilities": "Wi-Fi, Parking, Pool",
            "check_in_time": "15:00",
            "check_out_time": "11:00",
            "cancellation_policy": "Non-refundable",
            "student_discount": 5.00,
            "special_offers": "10% off on weekends",
            "tourist_spots": ['Museum', 'Park', 'Historic Site']
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
        self.hotel = Hotel.objects.create(user=self.user, hotel_name="Test Hotel", city="Test City", phone_number="+11234567890", zip="11201")

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
        response = self.client.get(self.url)
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
            description="A lovely place to stay",
            zip = "11201"
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
            phone_number="+11234567890",
            zip = "11201"
        )
        self.room = RoomsDescription.objects.create(
            hotel=self.hotel,
            room_type="Single",
            number_of_rooms=5,
            price_per_night=100.00
        )
        self.reservation = Reservation.objects.create(
            hotel = self.hotel,
            room = self.room,
            student = self.student,
            first_name = "John",
            last_name = "Doe",
            email = "johndoe@example.com",
            country = "Testland",
            phone_number = "+123456789",
            expected_arrival_time = "15:00",
            check_in_date = date.today().isoformat(),
            check_out_date = (date.today() + timedelta(days=2)).isoformat(),
            guests = 1
        )
        self.client.force_authenticate(user=self.student_user)

        self.booking_list_url = reverse('reservations-list')
        self.booking_detail_url = reverse('reservations-detail', kwargs={'pk': self.reservation.id})
        self.booking_cancel_url = reverse('reservations-cancel', kwargs={'pk': self.reservation.id})

    def test_room_booking_success(self):
        response = self.client.post(self.booking_list_url, {
            "hotel": self.hotel.id,
            "room": self.room.id,
            "student": self.student.id,
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "country": "Testland",
            "phone_number": "+123456789",
            "expected_arrival_time": "17:00",
            "check_in_date": date.today().isoformat(),
            "check_out_date": (date.today() + timedelta(days=2)).isoformat(),
            "guests": 1
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)
        self.assertEqual(response.data["message"], "Reservation created successfully!")

    def test_room_booking_invalid_dates(self):
        response = self.client.post(self.booking_list_url, {
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

    def test_update_reservation(self):
        response = self.client.put(self.booking_detail_url, {
            "hotel": self.hotel.id,
            "room": self.room.id,
            "student": self.student.id,
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "country": "Testland",
            "phone_number": "+123456789",
            "expected_arrival_time": "16:00",
            "check_in_date": date.today().isoformat(),
            "check_out_date": (date.today() + timedelta(days=2)).isoformat(),
            "guests": 1
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Reservation updated successfully!')

    def test_partial_update_reservation(self):
        data = {
            "room": self.room.id,
            "last_name": "Doeeeee",
            "guests": 2
        }
        response = self.client.patch(self.booking_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Reservation partially updated successfully!')

    def test_cancel_reservation(self):
        data = {
            'reason': 'Changed plans'
        }
        response = self.client.post(self.booking_cancel_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

# class ReviewViewTest(TestCase):
#     def setUp(self):
#         # Create groups
#         self.students_group = Group.objects.create(name='Students')
#         self.hotels_group = Group.objects.create(name='Hotels')
#
#         # Create users
#         self.student_user = User.objects.create_user(username='student', password='password123')
#         self.student_user.groups.add(self.students_group)
#         self.hotel_user = User.objects.create_user(username='hotel_manager', password='password123')
#         self.hotel_user.groups.add(self.hotels_group)
#
#         # Create a hotel
#         self.hotel = Hotel.objects.create(name='Hotel Test', user=self.hotel_user, zip="11201")
#
#         # Create a client instance
#         self.client = APIClient()
#
#     def test_create_review(self):
#         self.client.login(username='student', password='password123')
#         data = {
#             'hotel_id': self.hotel.id,
#             'review': 'Great place!'
#         }
#         response = self.client.post('/reviews/', data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#     def test_create_review_without_auth(self):
#         data = {
#             'hotel_id': self.hotel.id,
#             'review': 'Great place!'
#         }
#         response = self.client.post('/reviews/', data)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#     def test_update_review(self):
#         # Create a review
#         review = CustomerReviews.objects.create(hotel=self.hotel, student=self.student_user.student_profile,
#                                                 review='Good')
#         self.client.login(username='student', password='password123')
#         data = {
#             'review': 'Updated review!'
#         }
#         response = self.client.put(f'/reviews/{review.id}/', data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         review.refresh_from_db()
#         self.assertEqual(review.review, 'Updated review!')
#
#     def test_permissions(self):
#         self.client.login(username='hotel_manager', password='password123')
#         response = self.client.get('/reviews/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_delete_review(self):
#         review = CustomerReviews.objects.create(hotel=self.hotel, student=self.student_user.student_profile,
#                                                 review='Good')
#         self.client.login(username='student', password='password123')
#         response = self.client.delete(f'/reviews/{review.id}/')
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertFalse(CustomerReviews.objects.filter(id=review.id).exists())

class TopHotelsViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.student_user = User.objects.create_user(username='studentuser', password='password123')
        self.student = Student.objects.create(
            user=self.student_user,
            dob=date(2000, 1, 1),
            phone_number="+11234567290",
            address="456 Student Lane",
            university_name="Test University",
            date_joined=timezone.now()
        )
        self.client.force_authenticate(user=self.user)
        self.client.force_authenticate(user=self.student_user)

        # Create sample hotels
        for i in range(10):  # Creating 10 hotels to ensure we have more than 8 to test the limit
            user = User.objects.create_user(username=f'testuser{i + 1}', password='testpassword')# Creating 10 hotels to ensure we have more than 8 to test the limit
            self.client.force_authenticate(user=user)
            hotel = Hotel.objects.create(
                user=user,
                hotel_name=f'Hotel {i + 1}',
                address1=f'Address {i + 1}',
                description=f'Description for Hotel {i + 1}',
                facilities='Free WiFi, Pool',
                check_in_time='14:00',
                check_out_time='12:00',
                phone_number=f'123543789{i}',
                cancellation_policy='Free cancellation within 24 hours',
                student_discount=True,
                average_rating=5 - (i * 0.1),  # Different ratings
                zip="11204"
            )
            self.room = RoomsDescription.objects.create(
                hotel=hotel,
                room_type="Single",
                number_of_rooms=5,
                price_per_night=120.00,
                max_occupancy=2
            )
            CustomerReviews.objects.create(hotel=hotel, student=self.student, rating=4, review='Great stay!')

    def test_get_top_hotels(self):
        url = reverse('top-hotels')  # Assuming you have set the name of this URL pattern
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 8)  # Should return top 8 hotels


class HotelProfileEditAPIViewTest(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username='testuser', password='password123')

        # Create a hotel profile for the test user
        self.hotel = Hotel.objects.create(
                user=self.user,
                hotel_name=f'Hotel 1',
                address1=f'Address 1',
                description=f'Description for Hotel 1',
                facilities='Free WiFi, Pool',
                check_in_time='14:00',
                check_out_time='12:00',
                phone_number=f'1235437891',
                cancellation_policy='Free cancellation within 24 hours',
                student_discount=True,
                average_rating=5,  # Different ratings
                zip="11204"
            )

        # Initialize the API client and authenticate the user
        self.client = APIClient()
        self.client.login(username='testuser', password='password123')

        # Define the URL for the HotelProfileEditAPIView
        self.url = reverse('hotel-profile-edit')  # Assuming the view uses a URL like this

    def test_get_hotel_profile(self):
        """
        Test retrieving the authenticated user's hotel profile.
        """
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_hotel_profile(self):
        """
        Test partially updating the hotel profile and the related user fields.
        """
        data = {
            'hotel_name': 'Updated Hotel Name',  # Hotel field
        }

        response = self.client.patch(self.url, data, format='json')

        # Test that the response status is OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test the changes were applied to the hotel and user profile
        self.hotel.refresh_from_db()
        self.assertEqual(self.hotel.hotel_name, 'Updated Hotel Name')

    def test_put_hotel_profile(self):
        """
        Test fully updating the hotel profile and related user fields.
        """
        data = {
            'hotel_name': 'Hotel 1',
            'address1': 'Address 1',
            'description' : 'Description for Hotel 1',
            'facilities' : 'Free WiFi, Pool',
            'check_in_time' : '14:00',
            'check_out_time' : '12:00',
            'phone_number' : '1235437891',
            'cancellation_policy' : 'Free cancellation within 24 hours',
            'student_discount' : True,
            'average_rating' : 5,
            'zip' : '11204'
        }

        response = self.client.put(self.url, data, format='json')

        # Test that the response status is OK
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_unauthenticated_user(self):
        """
        Test that an unauthenticated user cannot access the hotel profile.
        """
        client = APIClient()  # A new client that is not authenticated
        response = client.get(self.url)

        # Test that the response status is Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CreatePaymentIntentViewTest(TestCase):

    def setUp(self):
        # Initialize the API client
        self.client = APIClient()

        # The endpoint URL for the CreatePaymentIntentView
        self.url = reverse('create-payment-intent')  # Adjust to your actual URL

    def test_create_payment_intent_success(self):
        """
        Test successful creation of a payment intent.
        """

        # Test data (valid request)
        data = {
            'amount': '2000',  # Amount in cents ($20.00)
            'currency': 'usd',
        }

        response = self.client.post(self.url, data, format='json')

        # Check the response status and returned client_secret
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_payment_intent_invalid_currency(self):
        """
        Test invalid currency in the payment intent request.
        """

        # Test data with invalid currency
        data = {
            'amount': 1500,  # Amount in cents ($15.00)
            'currency': 'invalid_currency',  # Invalid currency
        }

        response = self.client.post(self.url, data, format='json')

        # Check that a 400 error is returned
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class RoomViewSetTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

        # Create a test user and assign to 'Hotels' group
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.hotel_group = Group.objects.create(name='Hotels')
        self.user.groups.add(self.hotel_group)

        # Create a test hotel associated with the user
        self.hotel = Hotel.objects.create(
            user=self.user,
            hotel_name="Test Hotel",
            city="Test City",
            phone_number="+11234567890",
            zip="11201"
        )

        # Create a test room
        self.room = RoomsDescription.objects.create(
            hotel=self.hotel,
            room_type="Single",
            number_of_rooms=5,
            price_per_night=100.00
        )

    def test_view_rooms(self):
        url = reverse('rooms-list')  # Ensure the reverse name matches your URL patterns
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_room(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('rooms-list')
        data = {
            'room_type': 'Double',
            'number_of_rooms': '5',
            'price_per_night': '100.00',
            'facilities': 'Free WiFi, Pool',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_room(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('rooms-detail', kwargs={'pk': self.room.pk})
        data = {
            'hotel': self.room.hotel.id,
            'room_type': 'Double',
            'number_of_rooms': '7',
            'price_per_night': '200.00',
            'facilities': 'Free WiFi, Pool',
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_room(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('rooms-detail', kwargs={'pk': self.room.pk})
        data = {
            'price_per_night': '200.00',
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_room(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('rooms-detail', kwargs={'pk': self.room.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(RoomsDescription.objects.count(), 0)

    def test_permissions(self):
        url = reverse('rooms-list')
        data = {
            'room_number': '102',
            'room_type': 'Double'
        }
        # Test create without authentication
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class ReviewViewSetTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        # Create test groups
        self.student_group = Group.objects.create(name='Students')
        self.hotel_group = Group.objects.create(name='Hotels')

        # Create test users
        self.student_user = User.objects.create_user(username='student', password='password')
        self.student_user.groups.add(self.student_group)

        self.hotel_user = User.objects.create_user(username='hotel', password='password')
        self.hotel_user.groups.add(self.hotel_group)

        # Create test hotel
        self.hotel = Hotel.objects.create(
            user=self.hotel_user,
            hotel_name="Test Hotel",
            city="Test City",
            phone_number="+11234567890",
            zip="11201"
        )

        self.student = Student.objects.create(
            user=self.student_user,
            dob=date(2000, 1, 1),
            phone_number="+11234567290",
            address="456 Student Lane",
            university_name="Test University",
            date_joined=timezone.now()
        )

        # Create test review
        self.review = CustomerReviews.objects.create(
            hotel=self.hotel,
            student=self.student,
            rating=4,
            review="Great experience!",
            date_added=timezone.now()
        )

    def test_view_reviews(self):
        url = reverse('reviews-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_review(self):
        self.client.login(username='student', password='password')
        url = reverse('reviews-list')
        data = {
            'hotel': self.hotel.id,
            'hotel_id': self.hotel.id,
            'student': self.student.id,
            'rating': 4,
            'review': 'Nice stay!',
            'date_added': timezone.now()
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_review(self):
        self.client.login(username='student', password='password')
        url = reverse('reviews-detail', kwargs={'pk': self.review.pk})
        data = {
            'hotel': self.hotel.id,
            'student': self.student.id,
            'rating': 4,
            'review': 'Nice stay! yes',
            'date_added': timezone.now()
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_review(self):
        self.client.login(username='student', password='password')
        url = reverse('reviews-detail', kwargs={'pk': self.review.pk})
        data = {
            'rating': 3
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_review(self):
        self.client.login(username='student', password='password')
        url = reverse('reviews-detail', kwargs={'pk': self.review.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_permissions(self):
        url = reverse('reviews-list')
        data = {
            'hotel': self.hotel.id,
            'student': self.student.id,
            'rating': 4,
            'review': 'Nice stay! yes',
            'date_added': timezone.now()
        }
        # Test create without authentication
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)