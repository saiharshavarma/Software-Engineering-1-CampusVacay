from django.urls import path
from .views import StudentRegistration, StudentLogin, StudentLogout

# urlpatterns = [
#     path('register/', views.student_registration, name='student_registration'),
#     path('login/', views.student_login, name='student_login'),
#     path('logout/', views.student_logout, name='student_logout'),
# ]

from django.urls import path
from .views import UserRegistrationView, LogoutView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
<<<<<<< HEAD
    path('api/register/', StudentRegistration.as_view(), name='student-registration'),
    path('api/login/', StudentLogin.as_view(), name='student-login'),
    path('api/logout/', StudentLogout.as_view(), name='student-logout'),
=======
    path('api/register/', UserRegistrationView.as_view(), name='user-register'),
    path('api/login/', obtain_auth_token, name='api_login'),
    path('api/logout/', LogoutView.as_view(), name='api_logout'),
>>>>>>> api
]