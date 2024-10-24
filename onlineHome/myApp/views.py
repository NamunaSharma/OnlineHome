# from django.shortcuts import render

# # Create your views here.
# def home(request):
#     context={}
#     return render(request, "myApp/home.html",context)


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import BookingForm, RegistrationForm, ServiceProviderForm, CustomerForm
from .models import ServiceProvider, Customer,Service

# def register(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data['password'])
#             user.save()
            
#             role = form.cleaned_data['role']
#             if role == 'service_provider':
#                 service_provider_form = ServiceProviderForm(request.POST)
#                 if service_provider_form.is_valid():
#                     service_provider = service_provider_form.save(commit=False)
#                     service_provider.user = user
#                     service_provider.save()
#             else:
#                     customer_form = CustomerForm(request.POST)
#                     if customer_form.is_valid():
#                         customer = customer_form.save(commit=False)
#                         customer.user = user
#                         customer.save()

#             return redirect('login')  # Redirect to login page

#     else:
#         form = RegistrationForm()
    
#     return render(request, 'myApp/register.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            role = form.cleaned_data['role']
            if role == 'service_provider':
                service_provider_form = ServiceProviderForm(request.POST)
                if service_provider_form.is_valid():
                    service_provider = service_provider_form.save(commit=False)
                    service_provider.user = user
                    service_provider.save()
                else:
                    print(service_provider_form.errors)  # Debugging to show form errors
            elif role == 'customer':
                customer_form = CustomerForm(request.POST)
                if customer_form.is_valid():
                    customer = customer_form.save(commit=False)
                    customer.user = user
                    customer.save()
                else:
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
            print(form.errors)  # Debug: print form errors
    else:
        form = BookingForm()

    return render(request, 'myApp/Booking.html', {'form': form})


def services_view(request):
    services = Service.objects.all()  # Fetch all services from the database
    return render(request, 'MyApp/services.html', {'services': services})