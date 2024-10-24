from django.contrib import admin

from .models import Booking, Customer, Service, ServiceProvider,Category

# Register your models here.
admin.site.register(ServiceProvider)
admin.site.register(Service)
admin.site.register(Customer)
admin.site.register(Booking)
admin.site.register(Category)