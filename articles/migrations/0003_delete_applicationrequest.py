# Generated by Django 4.2.16 on 2024-11-03 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ApplicationRequest',
        ),
    ]