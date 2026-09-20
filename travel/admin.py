from django.contrib import admin
from .models import TourPackage, Booking, Payment

admin.site.register(TourPackage)
admin.site.register(Booking)
admin.site.register(Payment)
