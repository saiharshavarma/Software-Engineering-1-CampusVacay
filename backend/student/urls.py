from django.urls import path
from .views import StudentRegistration, StudentLogin, StudentLogout

urlpatterns = [
    path('api/register/', StudentRegistration.as_view(), name='student-registration'),
    path('api/login/', StudentLogin.as_view(), name='student-login'),
    path('api/logout/', StudentLogout.as_view(), name='student-logout'),
]