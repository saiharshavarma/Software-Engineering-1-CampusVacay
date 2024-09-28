from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.hotel_dashboard, name='hotel_dashboard'),
    path('register/', views.hotel_registration, name='hotel_registration'),
    path('<int:hotel_id>/rooms/', views.view_room_details, name='view_room_details'),
    path('<int:hotel_id>/room/add/', views.enter_new_room, name='add_room'),
    path('room/<int:room_id>/edit/', views.update_room, name='edit_room'),
    path('room/<int:room_id>/delete/', views.delete_room, name='delete_room'),
    path('<int:hotel_id>/reviews/', views.view_hotel_reviews, name='view_hotel_reviews'),
    path('<int:hotel_id>/review/add/', views.create_review, name='add_review'),
    path('review/<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
]