from django.urls import path
from .views import UserRegistrationView, LogoutView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('api/register/', UserRegistrationView.as_view(), name='user-register'),
    path('api/login/', obtain_auth_token, name='api_login'),
    path('api/logout/', LogoutView.as_view(), name='api_logout'),
]
