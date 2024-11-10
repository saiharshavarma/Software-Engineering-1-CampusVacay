from django.db import models
from django.contrib.auth.models import User, Group
from django.core.validators import RegexValidator
from django.utils import timezone
from django.db import migrations
from django.core.exceptions import ValidationError

def create_student_group(apps, schema_editor):
    Group.objects.get_or_create(name='Students')

class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(create_student_group),
    ]

def add_user_to_student_group(user):
    student_group, created = Group.objects.get_or_create(name='Students')
    user.groups.add(student_group)
    
# Create Student model
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    dob = models.DateField(verbose_name='Date of Birth')
    
    # Phone number with validation
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{10}$',
        message="Phone number must be entered in the format: '+19999999999'. It must have 10 digits after the country code."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=12, blank=True, verbose_name='Phone Number', unique=True)
    
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

    favorite_hotels = models.ManyToManyField('hotel.Hotel', related_name='favorite_students', blank=True)
    # Additional fields
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='Date Joined')

    def __str__(self):
        return f'{self.user.username} - Student Profile'

    def clean(self):
            super().clean()

            if self.phone_number:
                phone_digits = self.phone_number.replace('+', '').replace(' ', '').replace('-', '')
                
                if len(phone_digits) == 10:
                    self.phone_number = '+1' + phone_digits
                elif len(phone_digits) == 11 and phone_digits.startswith('1'):
                    self.phone_number = '+' + phone_digits
                else:
                    raise ValidationError("Phone number must have exactly 10 digits or start with '+1' followed by 10 digits.")