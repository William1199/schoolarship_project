# Generated by Django 4.2.16 on 2024-10-28 14:08

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField()),
                ('thumbnail', models.ImageField(upload_to='img')),
                ('admission_date', models.DateField()),
                ('entry_points', models.CharField(max_length=50)),
                ('diploma', models.CharField(max_length=50)),
                ('costs', models.CharField(max_length=50)),
                ('location', django_countries.fields.CountryField(max_length=2)),
                ('course_length', models.CharField(max_length=50)),
                ('information', models.TextField()),
                ('featured', models.BooleanField(default=False)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('updatedDate', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='articles_template', to='articles.category')),
            ],
        ),
    ]
