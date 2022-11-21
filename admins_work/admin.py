from django.contrib import admin

from .models import Userprofile, Rooms, Customer, ExtraServices, Booking

# Register your models here.
admin.site.register(Userprofile)
admin.site.register(Rooms)
admin.site.register(Customer)
admin.site.register(ExtraServices)
admin.site.register(Booking)
