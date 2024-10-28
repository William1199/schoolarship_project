from django.db import models
from django_countries.fields import CountryField
# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=25)

    def __str__(self):
        return self.title


class Articles(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to="img")
    admission_date = models.DateField()  # ngày nhập học
    entry_points = models.CharField(max_length=50)
    diploma = models.CharField(max_length=50)
    costs = models.CharField(max_length=50)
    location = CountryField()
    course_length = models.CharField(max_length=50)
    information = models.TextField()
    featured = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="articles_template")

    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title