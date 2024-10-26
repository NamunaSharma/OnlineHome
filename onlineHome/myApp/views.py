import math
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import BookingForm, RegistrationForm, ServiceProviderForm, CustomerForm
from .models import ServiceProvider, Customer,Service
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            role = form.cleaned_data['role']
            if role == 'service_provider':
                service_provider_form = ServiceProviderForm(request.POST,request.FILES)
                if service_provider_form.is_valid():
                    service_provider = service_provider_form.save(commit=False)
                    service_provider.user = user
                    service_provider.save()
                else:
                    print("Service Provider Form Errors:", ServiceProviderForm.errors)
                    print(service_provider_form.errors)  # Debugging to show form errors
            elif role == 'customer':
                customer_form = CustomerForm(request.POST,request.FILES)
                if customer_form.is_valid():
                    customer = customer_form.save(commit=False)
                    customer.user = user
                    customer.save()
                else:
                    print("Service Provider Form Errors:", CustomerForm.errors)
                    print(customer_form.errors)  # Debugging to show form errors

            return redirect('login')  # Redirect to login page

    else:
        form = RegistrationForm()
    
    return render(request, 'myApp/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Debug to check role
            if hasattr(user, 'serviceprovider'):
                print("User is a service provider")
                return redirect('service_provider')  # Redirect to service provider page
            elif hasattr(user, 'customer'):
                print("User is a customer")
                return redirect('booking')  # Redirect to customer page
            else:
                print("User role not found")
                return render(request, 'myApp/login.html', {'error': 'User role not found'})
        else:
            return render(request, 'myApp/login.html', {'error': 'Invalid credentials'})

    return render(request, 'myApp/login.html')

def service_provider(request):
    return render(request, 'myApp/service_provider.html')

def customer(request):
    return render(request, 'myApp/customer.html')


def create_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user.customer  # Associate with logged-in customer
            booking.save()
            return redirect('login')  # Redirect to a success page
        else:
            print("Service Provider Form Errors:", ServiceProviderForm.errors)
            print(form.errors)  # Debug: print form errors
    else:
        form = BookingForm()

    return render(request, 'myApp/Booking.html', {'form': form})


def services_view(request):
    services = Service.objects.all()  # Fetch all services from the database
    return render(request, 'MyApp/services.html', {'services': services})



def customer_profile(request, user_id):
    customer = Customer.objects.get(user__id=user_id)  # Fetch customer by user ID
    return render(request, 'myApp/customerpro.html', {'customer': customer})





#new

def euclidean_distance(coord1, coord2):
    """
    Calculate the Euclidean distance between two geographical points.

    :param coord1: Tuple (latitude1, longitude1)
    :param coord2: Tuple (latitude2, longitude2)
    :return: Distance between the two points
    """
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    return math.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)

def find_nearest_service_providers(user_location, service_providers, k=3):
    """
    Find the nearest service providers based on user location.

    :param user_location: Tuple (latitude, longitude)
    :param service_providers: List of service provider objects
    :param k: Number of nearest providers to return
    :return: List of nearest service providers
    """
    distances = []

    for provider in service_providers:
        provider_location = (provider.latitude, provider.longitude)
        distance = euclidean_distance(user_location, provider_location)
        distances.append((provider, distance))
        print(f"Provider: {provider.user.username}, Location: {provider_location}, Distance: {distance}")

    # Sort by distance and select the nearest k providers
    nearest_providers = sorted(distances, key=lambda x: x[1])[:k]
    return [provider for provider, distance in nearest_providers]

def book_service(request):
    if request.method == "POST":
        # Get the user location from the form
        location = request.POST.get('location')
        lat, lng = map(float, location.split(','))  # Split and convert to float
        
        # Get all service providers from the database
        service_providers = ServiceProvider.objects.all()

        # Find the nearest service providers
        user_location = (lat, lng)
        nearest_providers = find_nearest_service_providers(user_location, service_providers)

        # Render the results
        return render(request, 'MyApp/nearest_provider.html', {'nearest_providers': nearest_providers})

    return render(request, 'myApp/booking_form.html')