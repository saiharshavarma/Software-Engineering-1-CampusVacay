from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils import timezone

# Custom user model inheriting from Django's AbstractUser
class StudentUser(AbstractUser):
    username = models.CharField(max_length=30, unique=True, verbose_name='Username')
    email = models.EmailField(unique=True, verbose_name='Email Address')
    first_name = models.CharField(max_length=30, verbose_name='First Name')
    last_name = models.CharField(max_length=30, verbose_name='Last Name')
    dob = models.DateField(verbose_name='Date of Birth')

    # Phone number with validation
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,10}$',
        message="Phone number must be entered in the format: '+9999999999'. Up to 10 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True, verbose_name='Phone Number')

    address = models.TextField(verbose_name='Address', blank=True)

    # University details
    university_name = models.CharField(max_length=100, verbose_name='University Name')
    
    # University ID proof - Accepting file types such as image or PDF
    university_id_proof = models.FileField(
        upload_to='university_ids/',
        verbose_name='University ID Proof',
        help_text="Upload an image or PDF file",
        blank=True,
        null=True
    )

    # Additional fields
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='Date Joined')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.username} ({self.first_name} {self.last_name})'