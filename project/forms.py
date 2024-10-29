from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

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
    desired_study_country = CountryField().formfield(widget=CountrySelectWidget(attrs={
        'class': 'form-control',
        'id': 'id_desired_study_country'
    }))
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


class UpdateProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter firstname"}))
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter lastname"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter username"}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter email address"}))
    profile_pic = forms.ImageField(
        label='Profile picture',
        widget=forms.FileInput(attrs={"class": "form-control", "placeholder": "Upload image"}))
    dateOfBirth = forms.DateField(
        label='Date of Birth',
        widget=forms.DateInput(
            attrs={"class": "form-control", "placeholder": "Select your date of birth", "type": "date"}))
    address = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your address"}))
    phone = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your phone number"}))
    bio = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter your bio"}))
    role = forms.CharField(label='Your Position',
                           widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your role"}))

    # Các trường chỉ dành cho sinh viên
    gpa = forms.DecimalField(
        label='Your GPA',
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter GPA (0.0 - 4.0)"}))
    language_score = forms.DecimalField(
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter language score"}))
    language_certificate = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "form-control", "placeholder": "Upload language certificate"}))
    desired_study_country = CountryField().formfield(label="Desired study abroad country",
                                                     widget=CountrySelectWidget(attrs={
                                                         'class': 'form-control',
                                                         'id': 'id_desired_study_country'
                                                     }))
    degree_interest = forms.ChoiceField(
        choices=DEGREE_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = get_user_model()
        fields = [
            "first_name", "last_name", "username", "email", "dateOfBirth", "address", "bio",
            "phone", "role", "profile_pic", "gpa", "language_score", "language_certificate",
            "desired_study_country", "degree_interest"
        ]

    def __init__(self, *args, **kwargs):
        is_student = kwargs.pop('is_student', False)
        super(UpdateProfileForm, self).__init__(*args, **kwargs)

        if not is_student:
            # Ẩn các trường sinh viên nếu is_student là False
            self.fields['gpa'].widget.attrs['style'] = 'display: none;'
            self.fields['language_score'].widget.attrs['style'] = 'display: none;'
            self.fields['language_certificate'].widget.attrs['style'] = 'display: none;'
            self.fields['desired_study_country'].widget.attrs['style'] = 'display: none;'
            self.fields['degree_interest'].widget.attrs['style'] = 'display: none;'
