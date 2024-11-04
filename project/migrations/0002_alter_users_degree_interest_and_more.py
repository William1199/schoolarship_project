# Generated by Django 4.2.16 on 2024-11-03 16:08

import django.core.validators
from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='degree_interest',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='desired_study_country',
            field=django_countries.fields.CountryField(blank=True, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='gpa',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='GPA scale 0.0 - 4.0', max_digits=3, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(4.0)]),
        ),
    ]
