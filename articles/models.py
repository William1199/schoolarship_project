from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django_countries.fields import CountryField
from django.conf import settings


# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Articles(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
                             related_name="articles")
    title = models.CharField(max_length=500, unique=True)
    slug = models.SlugField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to="img")
    slot = models.IntegerField(blank=True, null=True)
    admission_date = models.DateField()  # ngày nhập học

    require_gpa = models.DecimalField(max_digits=3, decimal_places=2,
                              validators=[MinValueValidator(0.0), MaxValueValidator(4.0)],
                              help_text="GPA scale 0.0 - 4.0", blank=True, null=True)
    entry_language = models.CharField(max_length=50)
    entry_points = models.CharField(max_length=50)
    diploma_after_course = models.CharField(max_length=50)

    costs = models.CharField(max_length=50)
    location = CountryField()
    course_length = models.CharField(max_length=50)
    information = models.TextField()
    featured = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True,
                                 related_name="articles_template")

    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey(Articles, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return self.body


class ApplyRequest(models.Model):
    article = models.ForeignKey(Articles, on_delete=models.CASCADE, related_name="apply_requests")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=10,
                              choices=[('pending', 'Pending'), ('approved', 'Approved'), ('denied', 'Denied')],
                              default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} -> {self.article.title} ({self.status})"
