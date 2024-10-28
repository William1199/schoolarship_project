from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

DEGREE_CHOICES = [
    ('bachelor', "Bachelor's Degree"),
    ('master', "Master's Degree"),
    ('doctorate', "Doctorate Degree"),
]

class RegisterForm(UserCreationForm):
    email = forms.CharField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter email address"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter username"}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter password"}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm password"}))

    # Thêm trường is_student và các trường bổ sung cho sinh viên
    is_student = forms.BooleanField(required=False, label="Are you a student?", widget=forms.CheckboxInput())
    gpa = forms.DecimalField(
        max_digits=3, decimal_places=2, required=False,
        validators=[MinValueValidator(0.0), MaxValueValidator(4.0)],
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter Your GPA (0.0 - 4.0)"}))
    language_score = forms.DecimalField(
        max_digits=5, decimal_places=2, required=False,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter Your Language Score"}))
    language_certificate = forms.ImageField(required=False, widget=forms.FileInput(attrs={"class": "form-control"}))
    desired_study_country = forms.CharField(
        max_length=50, required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Your Desired Study Country"}))
    degree_interest = forms.ChoiceField(
        choices=DEGREE_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = get_user_model()
        fields = ["email", "username", "password1", "password2", "is_student", "gpa", "language_score",
                  "language_certificate", "desired_study_country", "degree_interest"]

    def clean(self):
        cleaned_data = super().clean()
        is_student = cleaned_data.get("is_student")

        # Kiểm tra các trường bổ sung nếu người dùng là sinh viên
        if is_student:
            if not cleaned_data.get("gpa"):
                self.add_error("gpa", "GPA is required for students.")
            if not cleaned_data.get("language_score"):
                self.add_error("language_score", "Language score is required for students.")
            if not cleaned_data.get("language_certificate"):
                self.add_error("language_certificate", "Language certificate is required for students.")

        return cleaned_data
