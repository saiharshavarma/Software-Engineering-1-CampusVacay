from django.urls import path, include
from . import views
from .views import UserRegistrationView, LogoutView, HotelSearchView, HotelManagerReservations, HotelDashboardView, HotelProfileEditAPIView#RoomBookingView, UpdateReservationView, CancelReservationView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet, RoomViewSet, CreatePaymentIntentView, ReservationViewSet, TopHotelsView


# urlpatterns = [
#     path('dashboard/', views.hotel_dashboard, name='hotel_dashboard'),
#     path('register/', views.hotel_registration, name='hotel_registration'),
#     path('login/', views.hotel_login, name='hotel_login'),
#     path('logout/', views.hotel_logout, name='hotel_logout'),
#     path('<int:hotel_id>/rooms/', views.view_room_details, name='view_room_details'),
#     path('<int:hotel_id>/room/add/', views.enter_new_room, name='add_room'),
#     path('room/<int:room_id>/edit/', views.update_room, name='edit_room'),
#     path('room/<int:room_id>/delete/', views.delete_room, name='delete_room'),
#     path('<int:hotel_id>/reviews/', views.view_hotel_reviews, name='view_hotel_reviews'),
#     path('<int:hotel_id>/review/add/', views.create_review, name='add_review'),
#     path('review/<int:review_id>/edit/', views.edit_review, name='edit_review'),
#     path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
# ]

router = DefaultRouter()
router.register(r'reviews', ReviewViewSet, basename='reviews')
router.register(r'rooms', RoomViewSet, basename='rooms')
router.register(r'reservations', ReservationViewSet, basename='reservations')

urlpatterns = [
    #path('api/dashboard/', views.hotel_dashboard, name='hotel_dashboard'),
    path('api/', include(router.urls)),
    path('api/register/', UserRegistrationView.as_view(), name='user-register'),
    path('api/login/', obtain_auth_token, name='api_login'),
    path('api/logout/', LogoutView.as_view(), name='api_logout'),

    path('api/top-hotels/', TopHotelsView.as_view(), name='top-hotels'),
    path('api/search/', HotelSearchView.as_view(), name='hotel-search'),
#    path('api/<int:hotel_id>/room/<int:room_id>/book/', RoomBookingView.as_view(), name='book-room'), extra path
    path('api/hotel/hotel-profile/', HotelProfileEditAPIView.as_view(), name='hotel-profile-edit'),
    path('api/hotel/reservations/', HotelManagerReservations.as_view(), name='hotel-reservations'),
    path('api/hotel/dashboard/', HotelDashboardView.as_view(), name='hotel-dashboard'),
#    path('api/reservation/<int:pk>/update/', UpdateReservationView.as_view(), name='update-reservation'),
#    path('api/reservation/<int:pk>/cancel/', CancelReservationView.as_view(), name='cancel-reservation'),
    path('api/payment/create-payment-intent/', CreatePaymentIntentView.as_view(), name='create-payment-intent'),


    # path('api/<int:hotel_id>/rooms/', views.view_room_details, name='view_room_details'),
    # path('api/<int:hotel_id>/room/add/', views.enter_new_room, name='add_room'),
    # path('api/room/<int:room_id>/edit/', views.update_room, name='edit_room'),
    # path('api/room/<int:room_id>/delete/', views.delete_room, name='delete_room'),
    # path('api/<int:hotel_id>/reviews/', views.view_hotel_reviews, name='view_hotel_reviews'),
    # path('api/<int:hotel_id>/review/add/', views.create_review, name='add_review'),
    # path('api/review/<int:review_id>/edit/', views.edit_review, name='edit_review'),
    # path('api/review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
]