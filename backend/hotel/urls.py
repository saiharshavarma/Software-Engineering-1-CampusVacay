from django.urls import path
from . import views
from .views import UserRegistrationView, LogoutView
from rest_framework.authtoken.views import obtain_auth_token

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

urlpatterns = [
    path('api/dashboard/', views.hotel_dashboard, name='hotel_dashboard'),
    path('api/register/', UserRegistrationView.as_view(), name='user-register'),
    path('api/login/', obtain_auth_token, name='api_login'),
    path('api/logout/', LogoutView.as_view(), name='api_logout'),
    path('api/<int:hotel_id>/rooms/', views.view_room_details, name='view_room_details'),
    path('api/<int:hotel_id>/room/add/', views.enter_new_room, name='add_room'),
    path('api/room/<int:room_id>/edit/', views.update_room, name='edit_room'),
    path('api/room/<int:room_id>/delete/', views.delete_room, name='delete_room'),
    path('api/<int:hotel_id>/reviews/', views.view_hotel_reviews, name='view_hotel_reviews'),
    path('api/<int:hotel_id>/review/add/', views.create_review, name='add_review'),
    path('api/review/<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('api/review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
]