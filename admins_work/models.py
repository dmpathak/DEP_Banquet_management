from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import CASCADE, PROTECT


# Create your models here.
class Userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    user_mobile = models.CharField(max_length=10)
    user_profile_photo = models.ImageField(upload_to='user_images/')
    user_address = models.CharField(max_length=20)
    user_postal_code = models.CharField(max_length=6)


Availability = [("Available", "Available"), ("NotAvailable", "NotAvailable")]
Types = [("AC", "AC"), ("NonAC", "NonAC")]


def valid_mobile(self, mob_number):
    if mob_number.value.match("/^\d{10}$/"):
        return mob_number
    else:
        ValidationError("mobile number should be...")


class Rooms(models.Model):
    room_name = models.CharField(max_length=20)
    room_status = models.CharField(max_length=20, choices=Availability)
    room_type = models.CharField(max_length=20, choices=Types)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.room_name + "(" + self.room_type + ")"


class Customer(models.Model):
    customer_name = models.CharField(max_length=20)
    customer_age = models.IntegerField()
    customer_address = models.CharField(max_length=20)
    customer_mobile = models.CharField(max_length=10, validators=[valid_mobile])

    def __str__(self):
        return self.customer_name


class ExtraServices(models.Model):
    service_name = models.CharField(max_length=20)
    service_price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return self.service_name


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=PROTECT)
    customer = models.ForeignKey(Customer, on_delete=PROTECT)
    rooms = models.ManyToManyField(Rooms)
    extra_service = models.ManyToManyField(ExtraServices, blank=True, null=True)
    CheckInDate = models.DateField()
    CheckOutDate = models.DateField()
