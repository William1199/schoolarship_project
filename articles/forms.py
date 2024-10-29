from django import forms
from .models import Articles, Category

DEGREE_CHOICES = [
    ('bachelor', "Bachelor's Degree"),
    ('master', "Master's Degree"),
    ('doctorate', "Doctorate Degree"),
]
class CreateArticleForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter title"})
    )
    slug = forms.SlugField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter slug (optional)"})
    )
    thumbnail = forms.ImageField(label="Article's picture",
                                 widget=forms.FileInput(attrs={"class": "form-control", "placeholder": "Add image"})
                                 )
    admission_date = forms.DateField(
        widget=forms.DateInput(attrs={"class": "form-control", "placeholder": "Enter admission date", "type": "date"})
    )
    entry_points = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter entry points"})
    )
    diploma = forms.ChoiceField(label="Diploma received after the course", choices=DEGREE_CHOICES,
                                widget=forms.Select(attrs={"class": "form-control"}))

    costs = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter costs"})
    )
    location = forms.ChoiceField(label="Location of study",
                                 choices=Articles._meta.get_field('location').get_choices(),
                                 widget=forms.Select(attrs={"class": "form-select", "placeholder": "Select location"})
                                 )
    course_length = forms.CharField(label="Course length",
                                    widget=forms.TextInput(
                                        attrs={"class": "form-control", "placeholder": "Enter course length"})
                                    )
    information = forms.CharField(label="Infotmation about schoolarship",
                                  widget=forms.Textarea(attrs={"class": "form-control",
                                                               "placeholder": "Enter detailed information about schoolarship"})
                                  )
    category = forms.ModelChoiceField(label="Type of Schoolarship",
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={"class": "form-select", "placeholder": "Select type"})
    )

    class Meta:
        model = Articles
        fields = [
        "title", "slug", "thumbnail", "admission_date", "entry_points", "diploma",
        "costs", "location", "course_length", "information", "category"
        ]