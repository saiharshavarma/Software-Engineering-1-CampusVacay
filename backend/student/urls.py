from . import views
from django.urls import path, include
from .views import UserRegistrationView, LogoutView, StudentSearchView, StudentProfileView, StudentReservationHistory, AddFavoriteHotelView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'favourite', AddFavoriteHotelView, basename='reservations')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/register/', UserRegistrationView.as_view(), name='student-user-register'),
    path('api/login/', obtain_auth_token, name='api_login'),
    path('api/logout/', LogoutView.as_view(), name='api_logout'),
    path('api/<int:hotel_id>/rooms/', views.view_room_details, name='view_room_details'),
    path('api/<int:hotel_id>/reviews/', views.view_hotel_reviews, name='view_hotel_reviews'),
    path('api/search/', StudentSearchView.as_view(), name='hotel-search'),
    path('api/student/profile/', StudentProfileView.as_view(), name='student-profile'),
    path('api/student/reservations/', StudentReservationHistory.as_view(), name='student-reservations'),
]
