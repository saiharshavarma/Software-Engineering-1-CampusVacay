from django.db import models
from django.contrib.auth.models import User, Group
from django.core.validators import RegexValidator
from django.utils import timezone
    
# Create Student model
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    dob = models.DateField(verbose_name='Date of Birth')
    
    # Phone number with validation
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{10,11}$',
        message="Phone number must be entered in the format: '+19999999999'. Up to 10 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=11, blank=True, verbose_name='Phone Number')
    
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

    def __str__(self):
        return f'{self.user.username} - Student Profile'