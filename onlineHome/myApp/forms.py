# In myApp/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import ServiceProvider, Customer,Booking,Review


class RegistrationForm(forms.ModelForm):
    role = forms.ChoiceField(choices=[('customer', 'Customer'), ('service_provider', 'Service Provider')])
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

class ServiceProviderForm(forms.ModelForm):
    class Meta:
        model = ServiceProvider
        fields = ['phone_number', 'service_type','longitude','latitude', 'experience_years','profile_picture']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['phone_number','longitude','latitude','profile_picture']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['location','booking_time']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }