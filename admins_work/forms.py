from datetime import datetime

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models import Q

from .models import Userprofile, Rooms, Customer, ExtraServices, Booking


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")

    def clean(self):
        user_mail = self.cleaned_data.get('email')
        validate_email(user_mail)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Userprofile
        exclude = ("user",)

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['user_mobile'].widget.attrs['class'] = 'form-control'
        self.fields['user_mobile'].widget.attrs['placeholder'] = 'Mobile:'
        self.fields['user_mobile'].label = 'mobile no'
        self.fields['user_mobile'].help_text = '<span class="form-text text-muted"><small>Required. Numbers only.</small></span>'

    def clean(self):
        user_mobile = self.cleaned_data.get('user_mobile')
        user_postal = self.cleaned_data.get("user_postal_code")


class RoomsForm(forms.ModelForm):
    class Meta:
        model = Rooms
        fields = "__all__"


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"


class ExtraServicesForm(forms.ModelForm):
    class Meta:
        model = ExtraServices
        fields = "__all__"


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        if 'instance' not in kwargs.keys():
            rooms = []
        else:
            rooms = kwargs['instance'].rooms.all()
        self.fields['rooms'].queryset = Rooms.objects.filter(Q(room_status="Available") | Q(id__in=[my_room.id for my_room in rooms]))

    def clean(self):
        checkin = self.cleaned_data.get('CheckInDate')
        checkout = self.cleaned_data.get('CheckOutDate')
        print("checkout", checkout)
        print(checkin)
        if checkin > checkout:
            raise ValidationError("checked out before checkin")

        if checkin < datetime.now().date():
            err = "Please add future date and time for checkin"
            self.add_error("CheckInDate", err)
        if checkout < datetime.now().date():
            err = "Please add future date and time for checkout"
            self.add_error("CheckOutDate", err)

