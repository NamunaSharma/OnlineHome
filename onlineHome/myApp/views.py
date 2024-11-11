from datetime import datetime, timedelta
from itertools import count
import json
import math
from pyexpat.errors import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from .forms import BookingForm, RegistrationForm, ReviewForm, ServiceProviderForm, CustomerForm
from .models import Booking, Category, ServiceProvider, Customer,Service
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Create the user object without saving to DB immediately
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()  # Save the user
            
            # Check the role and create the corresponding model instance
            role = form.cleaned_data['role']
            
            if role == 'service_provider':
                service_provider_form = ServiceProviderForm(request.POST, request.FILES)
                if service_provider_form.is_valid():
                    # Initialize ServiceProvider instance but don't save yet
                    service_provider = service_provider_form.save(commit=False)
                    service_provider.user = user
                    service_provider.is_approved = False  # Set is_approved explicitly to False
                    service_provider.save()  # Now save the instance
                    messages.success(request, "Registration successful as Service Provider")
                else:
                    messages.error(request, f"Service Provider form errors: {service_provider_form.errors}")
                    return redirect('register')
            else:  # It's a customer
                customer_form = CustomerForm(request.POST, request.FILES)
                if customer_form.is_valid():
                    customer = customer_form.save(commit=False)
                    customer.user = user  # Link the user to the customer model
                    customer.save()
                    messages.success(request, "Registration successful as Customer")
                else:
                    messages.error(request, f"Customer form errors: {customer_form.errors}")
                    return redirect('register')

            # Log the user in automatically after registration
            login(request, user)
            return redirect('login')  # Redirect to 'home' or dashboard page
        else:
            messages.error(request, f"Registration form errors: {form.errors}")
            return redirect('register')
    else:
        form = RegistrationForm()
    return render(request, 'myApp/register.html', {'form': form})

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ServiceProvider

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Check if the user is a service provider
            if hasattr(user, 'serviceprovider'):
                service_provider = user.serviceprovider
                if not service_provider.is_approved:
                    messages.error(request, "Your account is awaiting admin approval.")
                    return redirect('login')
                else:
                    # Proceed if the service provider is approved
                    login(request, user)
                    return redirect('service_provider')  # Redirect to service provider page
            elif hasattr(user, 'customer'):
                # Proceed if the user is a customer
                login(request, user)
                return redirect('customer')  # Redirect to customer page
            else:
                # Handle case where user role is not found
                messages.error(request, "User role not found.")
                return redirect('login')
        else:
            # If authentication fails, show an error message
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'myApp/login.html')

def service_provider(request):
        provider_id = request.user.id
    # Fetch the provider's information using the provider's ID
        provider = ServiceProvider.objects.get(user_id=provider_id)

        return render(request, 'myApp/serviceprofile.html', {'provider': provider})

def customer(request):
    return render(request, 'myApp/customer.html')

from django.shortcuts import render, get_object_or_404, redirect
from .models import Service, ServiceProvider, Booking

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Service, ServiceProvider, Booking


def cosine_similarity_manual(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

@login_required  # Ensure the user is logged in
def create_booking(request, service_id=None):
    service = None
    recommendations = []  
    if service_id:
        service = get_object_or_404(Service, id=service_id)
        recommendations = recommend_services(request, service.id)

    elif 'service_id' in request.GET:
        service_id = request.GET['service_id']
        service = get_object_or_404(Service, id=service_id)
        recommendations = recommend_services(request, service.id)

    if request.method == 'POST':
        location = request.POST.get('location')  # Retrieve the location from the form
        provider_id = request.POST.get('provider_id')  # Retrieve the provider ID from the form
        booking_time = request.POST.get('booking_time')  # Retrieve the booking time from the form

        print(f"Received provider ID: {provider_id}")  # Check that you're receiving the correct provider ID

        # Find the service provider by ID
        try:
            provider = ServiceProvider.objects.get(id=provider_id)
        except ServiceProvider.DoesNotExist:
            provider = None  # Handle the case where no provider is found

        # Ensure the user has a 'customer' instance
        try:
            customer = request.user.customer  # Assuming a OneToOne relationship between User and Customer
        except AttributeError:
            customer = None  
        existing_booking = Booking.objects.filter(provider=provider, booking_time=booking_time)
        if existing_booking.exists():
            # Handle the case where the provider is already booked at this time
            return render(request, 'myApp/Booking.html', {
                'service': service,
                'recommendations': recommendations,
                'error': "This provider is already booked at the selected time. Please choose another time.",
            })

        if customer and provider:
            # Create and save the booking if both customer and provider are valid
            booking = Booking.objects.create(
                location=location,
                booking_time=booking_time,
                customer=customer,
                provider=provider,
                service=service,
            )
            booking.save()  # Save the booking to the database
            return redirect('categories')  # Replace with actual URL name

        else:
            return redirect('customer')  # Handle this with a proper error page or message

    else:
        return render(request, 'myApp/Booking.html', {'service': service,'recommendations': recommendations })


def services_view(request):
    services = Service.objects.all()  # Fetch all services from the database
    return render(request, 'MyApp/services.html', {'services': services})

from django.db.models import Count
from datetime import datetime, timedelta
from django.db.models.functions import TruncDay

def provider_profile(request, provider_id):
    provider = ServiceProvider.objects.get(user_id=provider_id)
    
    reviews = provider.reviews.all()
    
    # Calculate the average rating
    if reviews.exists():
        total_rating = sum([review.rating for review in reviews])
        average_rating = total_rating / len(reviews)
    else:
        average_rating = 0  # Default to 0 if no reviews

    # Calculate filled and empty stars
    filled_stars = int(average_rating)
    empty_stars = 5 - filled_stars
    last_week = datetime.now() - timedelta(days=7)
    completed_services = (
        provider.bookings.filter(service_completed=True, booking_time__gte=last_week)
        .annotate(day=TruncDay('booking_time'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )
    services_by_day = {entry['day'].strftime('%a'): entry['count'] for entry in completed_services}

    context = {
        'provider': provider,
        'reviews': reviews,
        'average_rating': average_rating,
        'filled_stars': range(filled_stars),
        'empty_stars': range(empty_stars),
        'services_by_day': services_by_day,
    }

    return render(request, 'myApp/serviceprofile.html', context)

def customer_profile(request, user_id):
    customer = Customer.objects.get(user__id=user_id)  
    bookings = Booking.objects.filter(customer=customer)# Fetch customer by user ID
    return render(request, 'myApp/customerpro.html', {'customer': customer,'bookings': bookings})


def category_view(request):
    categories = Category.objects.all()  # Fetch all services from the database
    return render(request, 'MyApp/categories.html', {'categories': categories})

#new
import math

def haversine_distance(coord1, coord2):
    """
    Calculate the Haversine distance between two geographical points.
    
    :param coord1: Tuple (latitude1, longitude1)
    :param coord2: Tuple (latitude2, longitude2)
    :return: Distance between the two points in kilometers
    """
    # Radius of the Earth in kilometers
    R = 6371.0
    
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Differences in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Distance in kilometers
    distance = R * c
    return distance
def find_nearest_service_providers(user_location, service_providers, max_distance_km=50, k=3):
    """
    Find the nearest service providers based on user location using the Haversine formula.
    
    :param user_location: Tuple (latitude, longitude)
    :param service_providers: List of service provider objects
    :param max_distance_km: Maximum distance (in km) to consider a provider as "nearby"
    :param k: Number of nearest providers to return
    :return: List of nearest service providers or a message if no providers are nearby
    """
    distances = []

    for provider in service_providers:
        provider_location = (provider.latitude, provider.longitude)
        distance = haversine_distance(user_location, provider_location)
        
        # If the provider is within the max distance, add to the list
        if distance <= max_distance_km:
            distances.append((provider, distance))

    # If no providers are found within the maximum distance
    if not distances:
        return None

    # Sort by distance and select the nearest k providers
    nearest_providers = sorted(distances, key=lambda x: x[1])[:k]
    return [provider for provider, distance in nearest_providers]



def get_nearby_providers(request):
    lat = float(request.GET.get('lat'))
    lon = float(request.GET.get('lng'))

    # Get all service providers from the database
    service_providers = ServiceProvider.objects.all()


    # Find nearest providers using the haversine distance logic
    nearest_providers = find_nearest_service_providers((lat, lon), service_providers)

    if nearest_providers is None:
        return JsonResponse({'providers': []})

    # Create a list of dictionaries for the providers
    providers = [
        {
            'id': provider.id,
            'name': provider.user.username,
            'profile_picture': provider.profile_picture.url,
            'latitude': provider.latitude,
            'longitude': provider.longitude,
            'rating': provider.average_rating if isinstance(provider.average_rating, float) else provider.average_rating(),
            'experience_years': provider.experience_years,
        }
        for provider in nearest_providers
    ]
    return JsonResponse({'providers': providers})


    ##recommendation
from .models import Service
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd

# def cosine_similarity_manual(v1, v2):
#     dot_product = np.dot(v1, v2)
#     norm_v1 = np.linalg.norm(v1)
#     norm_v2 = np.linalg.norm(v2)
#     return dot_product / (norm_v1 * norm_v2)

def recommend_services(request, service_id):
    # Fetch all services
    services = Service.objects.all()
    
    # Extract relevant attributes for each service
    data = pd.DataFrame({
        'id': [service.id for service in services],
        'description': [service.description for service in services],
    })
    
    # Vectorize descriptions
    vectorizer = TfidfVectorizer()
    description_matrix = vectorizer.fit_transform(data['description'])
    
    # Combine features (you can include ratings or other features if needed)
    combined_features = description_matrix.toarray()
    
    # Get the feature vector for the target service
    service_idx = data[data['id'] == service_id].index[0]
    target_vector = combined_features[service_idx]
    
    # Manually calculate cosine similarity with other services
    similarity_scores = []
    for i, vector in enumerate(combined_features):
        if i != service_idx:  # skip the target service itself
            similarity = cosine_similarity_manual(target_vector, vector)
            similarity_scores.append((i, similarity))
    
    # Sort by similarity score, descending
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)[:5]
    
    # Fetch recommended service IDs
    recommended_indices = [i[0] for i in similarity_scores]
    recommended_services = Service.objects.filter(id__in=[data['id'][i] for i in recommended_indices])
    
    return recommended_services  # Return the recommended services directly


def category_services(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    query = request.GET.get('search', '')
    if query:
        services = Service.objects.filter(
            category=category,
            title__icontains=query
        )
    else:
        services = Service.objects.filter(category=category)
    return render(request, 'MyApp/category_services.html', {
        'category': category,
        'services': services
    })

def booking(request, service_id=None):
    service = None
    if service_id:
        service = get_object_or_404(Service, id=service_id)
    elif 'service_id' in request.GET:
        service_id = request.GET['service_id']
        service = get_object_or_404(Service, id=service_id)
    return render(request, 'myApp/Booking.html', {'service': service})



@login_required
def service_provider(request):
    # Fetch the provider's information using the logged-in user's ID
    provider_id = request.user.id
    provider = get_object_or_404(ServiceProvider, user_id=provider_id)
    
    return render(request, 'myApp/service_provider.html', {'provider': provider})

from django.db.models import Q

@login_required
def provider_bookings(request, provider_id):
    provider = get_object_or_404(ServiceProvider, user_id=provider_id)
    
    # Ensure the logged-in user is the provider
    if request.user != provider.user:
        return redirect('login')
    
    # Get sorting order from URL parameters
    sort_order = request.GET.get('sort', 'asc')
    
    # Get search and status filter parameters
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    # Filter bookings based on search query and status
    bookings = Booking.objects.filter(provider=provider)
    
    if search_query:
        bookings = bookings.filter(
            Q(service__title__icontains=search_query) | 
            Q(customer__user__username__icontains=search_query)
        )
    
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    if sort_order == 'desc':
        bookings = bookings.order_by('-booking_time')
    else:
        bookings = bookings.order_by('booking_time')
    
    return render(request, 'myApp/provider_bookings.html', {
        'provider': provider,
        'bookings': bookings,
        'sort_order': sort_order,
        'search': search_query,
        'status': status_filter,
    })

@login_required
def confirm_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    # Ensure the logged-in user is the provider and the status is 'confirmed'
    if request.user != booking.provider.user:
        return redirect('login')

    if request.method == "POST":
        if booking.status == "pending":
            # Confirm the booking
            booking.status = "confirmed"
            booking.save()
            messages.success(request, "Booking confirmed successfully.")
        elif booking.status == "confirmed":
            # Allow only the provider to mark the booking as completed
            if booking.service_completed:
                booking.status = "completed"
                booking.save()
                messages.success(request, "Booking marked as completed.")
            else:
                messages.error(request, "Please confirm that the service was provided before marking it as completed.")
        else:
            messages.error(request, "Invalid action.")

    return render(request, 'myApp/provider_bookings.html', {
        'bookings': Booking.objects.filter(provider=booking.provider),
        'provider': booking.provider,
        'sort_order': request.GET.get('sort', 'asc'),
        'search': request.GET.get('search', ''),
        'status': request.GET.get('status', '')
    })


#     return render(request, 'myApp/submit_review.html', context)
@login_required
def mark_service_completed(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Ensure the logged-in user is the provider
    if request.user != booking.provider.user:
        return redirect('login')
    
    # Ensure the booking status is confirmed before marking it completed
    if booking.status == "confirmed":
        booking.status = "completed"
        booking.service_completed = True
        booking.needs_review = True
        booking.save()
        messages.success(request, "Service marked as completed.")
        print(booking.status)
    else:
        messages.error(request, "Booking is not confirmed yet.")
    
    return render(request, 'myApp/provider_bookings.html', {
        'bookings': Booking.objects.filter(provider=booking.provider),
        'provider': booking.provider,
        'sort_order': request.GET.get('sort', 'asc'),
        'search': request.GET.get('search', ''),
        'status': request.GET.get('status', '')
    })


@login_required
def user_booking_list(request):
    # Get the customer object for the current logged-in user
    customer = Customer.objects.get(user=request.user)  # Assuming 'Customer' model has a ForeignKey to User

    # Find the booking that needs a review
    pending_review_booking = Booking.objects.filter(
        customer=customer,  # Use customer instance, not user instance
        status='completed',
        needs_review=True
    ).first()
    

    if pending_review_booking:
     print(f"Redirecting to submit_review for booking {pending_review_booking.id}")
     return redirect('submit_review', booking_id=pending_review_booking.id)
    else:
     print("No pending review booking found.")


    # Render all bookings if no pending reviews
    bookings = Booking.objects.filter(customer=customer)  # Use customer instance here as well
    return render(request, 'myApp/customer.html', {'bookings': bookings})


@login_required
def submit_review(request, booking_id):
    # Fetch the booking by booking_id
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Ensure the booking is completed and needs a review
    if booking.status != 'completed' or not booking.needs_review:
        messages.error(request, "This booking cannot be reviewed yet.")
        return redirect('user_booking_list')
    
    # If the method is POST, process the review form
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        
        if form.is_valid():
            # Create a new review without saving to DB yet
            review = form.save(commit=False)
            
            # Assign the booking and provider to the review
            review.booking = booking
            review.provider = booking.provider
            review.customer = request.user.customer  # Assuming the customer is linked to the user
            
            # Save the review to the database
            review.save()
            
            # Mark the booking as reviewed
            booking.needs_review = False
            booking.save()
            
            # Show a success message and redirect to the provider profile
            messages.success(request, "Review submitted successfully.")
            # return redirect('provider_profile', provider_id=booking.provider.id)
            return redirect('customer')
    else:
        form = ReviewForm()

    # Context to pass to the template
    context = {
        'form': form,
        'booking': booking,
        'provider': booking.provider,  # Pass the provider object as well
    }
    
    # Render the review submission template
    return render(request, 'myApp/submit_review.html', context)


from django.utils.dateparse import parse_datetime
def check_provider_availability(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        provider_id = data.get('provider_id')
        booking_time = data.get('booking_time')
        
        # Parse the datetime string into a datetime object
        booking_time = parse_datetime(booking_time) # type: ignore

        # Check if there is an existing booking for the provider at the given time
        existing_booking = Booking.objects.filter(
            provider_id=provider_id, 
            booking_time__date=booking_time.date()
        ).exists()

        # Return a JSON response with the availability status
        return JsonResponse({'is_available': not existing_booking})