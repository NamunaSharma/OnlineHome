# Generated by Django 5.1.2 on 2024-11-11 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0003_booking_needs_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceprovider',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
