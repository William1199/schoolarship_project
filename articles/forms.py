from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from .models import Articles, Category, Comment

DEGREE_CHOICES = [
    ('bachelor', "Bachelor's Degree"),
    ('master', "Master's Degree"),
    ('doctorate', "Doctorate Degree"),
]

LANGUAGE_TYPE_CHOICES = [
    ('ielts', "IELTS"),
    ('toeic', "TOEIC"),
    ('hsk', "HSK"),
    ('tcf', "TCF"),
    ('toefl', "TOEFL"),
    ('jlpt', "JLPT"),
    ('goethe', "Goethe Zertifikat"),
    ('dele', "DELE"),
    ('dalf', "DALF"),
    ('cils', "CILS"),
    ('celi', "CELI"),
    ('telc', "TELC"),
    ('cae', "Cambridge English: Advanced (CAE)"),
    ('fce', "Cambridge English: First (FCE)"),
    ('ptev', "PTE Academic"),
    ('dsh', "DSH"),
    ('nat-test', "NAT-TEST"),
]

class CreateArticleForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter title"})
    )
    thumbnail = forms.ImageField(label="Article's picture",
                                 widget=forms.FileInput(attrs={"class": "form-control", "placeholder": "Add image"})
                                 )
    admission_date = forms.DateField(
        widget=forms.DateInput(attrs={"class": "form-control", "placeholder": "Enter admission date", "type": "date"})
    )
    slot = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "Enter slot number",
            "type": "number",  # Đảm bảo đây là trường số trong HTML
            "min": "1",  # Đặt giá trị tối thiểu nếu muốn
        })
    )
    require_gpa = forms.DecimalField(
        max_digits=3, decimal_places=2, required=False,
        validators=[MinValueValidator(0.0), MaxValueValidator(4.0)],
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Required GPA (0.0 - 4.0)"}))

    entry_language = forms.ChoiceField(label="Required Language Type", choices=LANGUAGE_TYPE_CHOICES,
                                             widget=forms.Select(attrs={"class": "form-control"}))
    entry_points = forms.CharField(label="Required Language Score",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter entry points"})
    )

    diploma_after_course = forms.ChoiceField(label="Diploma received after the course", choices=DEGREE_CHOICES,
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
    information = forms.CharField(label="Information about schoolarship",
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
        "title", "thumbnail", "admission_date", "slot", "require_gpa", "entry_language", "entry_points", "diploma_after_course",
        "costs", "location", "course_length", "information", "category"
        ]

class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Say something about the article"}))
    class Meta:
        model=Comment
        fields = ['body']