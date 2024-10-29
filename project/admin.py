from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Users
# Register your models here.

class Admin(UserAdmin):
    list_display = [field.name for field in Users._meta.get_fields() if not field.is_relation]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2"),
            },
        ),
    )
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': (
        'first_name', 'last_name', 'dateOfBirth', 'address', 'phone', 'role', 'bio', 'is_student', 'gpa',
        'language_score', 'language_certificate', 'desired_study_country', 'degree_interest')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

admin.site.register(Users,Admin)