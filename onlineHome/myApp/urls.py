from . import views
from django.urls import path
from .views import register, login_view,create_booking,services_view

urlpatterns = [
    # path("",views.home, name= "home"),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('serviceprovider/', views.service_provider, name='service_provider'),
    path('customer/', views.customer, name='customer'),
    path('booking/', views.create_booking, name='booking'),
    path('services/', views.services_view, name='services'),

]
