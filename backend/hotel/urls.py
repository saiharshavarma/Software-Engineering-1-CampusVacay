from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.hotel_registration, name='hotel_registration'),
]