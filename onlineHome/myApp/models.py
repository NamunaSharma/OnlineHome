from django.db import models
from django.contrib.auth.models import User

# ServiceProvider Model
class ServiceProvider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    service_type = models.CharField(max_length=50, choices=[
        ('plumber', 'Plumber'),
        ('electrician', 'Electrician'),
        ('cleaner', 'Cleaner'),
        ('carpenter', 'Carpenter'),
    ])
    experience_years = models.PositiveIntegerField()
    latitude = models.FloatField(default=00.0)
    longitude = models.FloatField( default=00.0)
    profile_picture = models.ImageField(upload_to='provider_profiles/', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.service_type}'

# Customer Model
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    latitude = models.FloatField(default=00.0)
    longitude = models.FloatField( default=00.0)
    profile_picture = models.ImageField(upload_to='customer_profiles/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Service(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="services",default=1)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images/', default='images/electrician.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Booking(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='bookings')
    # service = models.ForeignKey('Service', on_delete=models.CASCADE)
    booking_time = models.DateTimeField()
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    # Additional fields
    name = models.CharField(max_length=100,default=" Janvii")
    email = models.EmailField(default='name@example.com')
    phone_number = models.CharField(max_length=15, default=9840332134)
    location = models.CharField(max_length=100, default="Koteshwor")

    def __str__(self):
        return f'Booking by {self.name} for {self.booking_time}'


