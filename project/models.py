from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Users(AbstractUser):
    email = models.EmailField(unique=True)
    profile_pic = models.ImageField(upload_to="p_img", blank=True, null=True)
    address = CountryField()
    phone = models.CharField(max_length=15, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    is_student = models.BooleanField(default=False)

    # Fields for students only
    gpa = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(0.0), MaxValueValidator(4.0)], help_text="GPA scale 0.0 - 4.0", null=True)
    language_score = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    language_certificate = models.ImageField(upload_to="language_certificate", null=True)

    desired_study_country = CountryField(null=True)
    degree_interest = models.CharField(max_length=50, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    def __str__(self):
        return self.email