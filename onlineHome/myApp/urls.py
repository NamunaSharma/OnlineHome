from . import views
from django.urls import path
from .views import register, login_view,create_booking,services_view,recommend_services,provider_bookings,submit_review,mark_service_completed,check_provider_availability
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path("",views.home, name= "home"),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
 path('serviceprovider/', views.service_provider, name='service_provider'),  # This serves the logged-in provider's profile
    path('serviceprovider/<int:provider_id>/', views.provider_profile, name='provider_profile'),  # Dynamic URL for specific provider pr
    path('customer/', views.customer, name='customer'),
    path('services/', views.services_view, name='services'),
    path('accounts/<int:user_id>/', views.customer_profile, name='customer_profile') ,
 path('get_nearby_providers', views.get_nearby_providers, name='get_nearby_providers'),
    # path('nearest/',views.book_service, name='nearest'),
    # path('booking/<int:provider_id>/', views.create_booking, name='booking'),
    path('booking/<int:service_id>/', views.create_booking, name='booking'),
   #  path('booking/<int:service_id>/', views.booking_view, name='booking_view'),
    # path('booking/<int:booking_id>/', views.create_booking, name='booking_by_id'),
    path('categories/', views.category_view, name='categories'),
    path('category/<int:category_id>/services/', views.category_services, name='category_services'),
    path('recommendations/<int:service_id>/', views.recommend_services, name='recommend_services'),
    path('provider/bookings/<int:provider_id>/', views.provider_bookings, name='provider_bookings'),
        # This is the bookings URL
   path('confirm-booking/<int:booking_id>/', views.confirm_booking, name='confirm_booking'),

   # path('provider/<int:provider_id>/review/', views.submit_review, name='submit_review'),
    path('mark_service_completed/<int:booking_id>/', views.mark_service_completed, name='mark_service_completed'),
    path('user/bookings/', views.user_booking_list, name='user_booking_list'),
   #  path('booking/<int:booking_id>/review/', views.submit_review, name='submit_review'),
   path('submit-review/<int:booking_id>/', views.submit_review, name='submit_review'),
   path('check_availability/', views.check_provider_availability, name='check_availability'),



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)