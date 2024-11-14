from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Users(AbstractUser):
    email = models.EmailField(unique=True)
    profile_pic = models.ImageField(upload_to="p_img", blank=True, null=True)
    dateOfBirth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=15, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    is_student = models.BooleanField(default=False)

    # Fields for students only
    gpa = models.DecimalField(max_digits=3, decimal_places=2,
                              validators=[MinValueValidator(0.0), MaxValueValidator(4.0)],
                              help_text="GPA scale 0.0 - 4.0", blank=True, null=True)
    language_type = models.CharField(max_length=50, null=True, blank=True)
    language_score = models.CharField(max_length=50, null=True, blank=True)
    language_certificate = models.ImageField(upload_to="language_certificate", null=True)

    desired_study_country = CountryField(blank=True, null=True)
    degree_interest = models.CharField(max_length=50, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    def __str__(self):
        return self.email