from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

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
    
    @property
    def average_rating(self):
        return self.reviews.aggregate(average=Avg('rating'))['average'] or 0.0

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
    image = models.ImageField(upload_to='images/', default='images/electrician.jpg')
    def __str__(self):
        return self.name
    

class Service(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="services",default="cleaning")
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images/', default='images/electrician.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Booking(models.Model):
    email = models.EmailField(null=True, blank=True) 
    location = models.CharField(max_length=255)
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='bookings', default=8)  # Assuming 1 is a valid ServiceProvider ID
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bookings')
    service = models.ForeignKey('Service', on_delete=models.CASCADE, default=1)
    booking_time = models.DateTimeField()
    needs_review = models.BooleanField(default=False)
    service_completed = models.BooleanField(default=False)
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Booking by {self.customer.user.username} for {self.customer.user.email}'
    
    

class Review(models.Model):
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reviews')
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(default=0)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.customer.user.username} for {self.provider.user.username} - {self.rating}/5'
