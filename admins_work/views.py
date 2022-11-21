import datetime

from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from .forms import UserProfileForm, UserForm, RoomsForm, ExtraServicesForm, BookingForm, CustomerForm
from .models import Customer, Rooms, ExtraServices, Booking


# Create your views here.
def user_index(request):
    if request.POST:
        user_profile_form = UserProfileForm(request.POST)
        user_form = UserForm(request.POST)
        if user_profile_form.is_valid() and user_form.is_valid():
            user_profile_form.save()
            user_form.save()
            user_profile_form = UserProfileForm()
            user_form = UserForm()
    else:
        user_profile_form = UserProfileForm()
        user_form = UserForm()
    return render(request, "user_templates/user_index.html",
                  {"user_form": user_form, "user_profile_form": user_profile_form})


def view_rooms(request):
    all_rooms = Rooms.objects.all()
    my_pagination = Paginator(all_rooms, 5)

    page_number = request.GET.get('page', 1)
    page_obj = my_pagination.page(page_number)
    return render(request, "user_templates/my_rooms.html", {"page_obj": page_obj})


def add_rooms(request):
    if request.POST:
        rooms_form = RoomsForm(request.POST)
        if rooms_form.is_valid():
            rooms_form.save()
            rooms_form = RoomsForm()
            return redirect(view_rooms)
    else:
        rooms_form = RoomsForm()
    return render(request, "user_templates/add_rooms.html", {"rooms_form": rooms_form})


def update_rooms(request, update_id):
    room_tobe_updated = get_object_or_404(Rooms, pk=update_id)
    print("room_tobe_updated", room_tobe_updated.room_status)
    if request.POST:
        room_form = RoomsForm(request.POST, instance=room_tobe_updated)
        # print("room_form", room_form)
        if room_form.is_valid():
            """ room_tobe_updated and initial_instance same j 6e to pan initial_instance j work kare 6e olu nahi why ????"""
            initial_instance = get_object_or_404(Rooms, pk=update_id)
            print("initial_instance", initial_instance.room_status)
            flag = 0
            if initial_instance.room_status == "NotAvailable" and room_form.cleaned_data["room_status"] == "Available":
                for each_booking in initial_instance.booking_set.all():
                    if each_booking.CheckOutDate >= datetime.datetime.now().date():
                        flag = 1
            if not flag:
                room_form.save()
            else:
                print("status not updated")
            return redirect(view_rooms)
    else:
        room_form = RoomsForm(instance=room_tobe_updated)
    return render(request, "user_templates/update_room.html", {"room_form": room_form, "update_id": update_id})


def delete_rooms(request, delete_id):
    room_tobe_deleted = get_object_or_404(Rooms, pk=delete_id)
    room_tobe_deleted.delete()
    return redirect(view_rooms)


def view_extra_services(request):
    all_services = ExtraServices.objects.all()
    my_pagination = Paginator(all_services, 5)

    page_number = request.GET.get('page', 1)
    page_obj = my_pagination.page(page_number)
    return render(request, "user_templates/my_extra_services.html", {"page_obj": page_obj})


def add_extra_services(request):
    if request.POST:
        extra_service_form = ExtraServicesForm(request.POST)
        if extra_service_form.is_valid():
            extra_service_form.save()
            extra_service_form = ExtraServicesForm()
            return redirect(view_extra_services)
    else:
        extra_service_form = ExtraServicesForm()
    return render(request, "user_templates/add_extra_services.html", {"extra_service_form": extra_service_form})


def update_extra_services(request, update_id):
    services_tobe_updated = get_object_or_404(ExtraServices, pk=update_id)
    if request.POST:
        services_form = ExtraServicesForm(request.POST, instance=services_tobe_updated)
        if services_form.is_valid():
            services_form.save()
            return redirect(view_extra_services)
    else:
        services_form = ExtraServicesForm(instance=services_tobe_updated)
    return render(request, "user_templates/update_service.html",
                  {"services_form": services_form, "update_id": update_id})


def delete_extra_services(request, delete_id):
    services_tobe_deleted = get_object_or_404(ExtraServices, pk=delete_id)
    services_tobe_deleted.delete()
    return redirect(view_extra_services)


def view_booking(request):
    all_bookings = Booking.objects.all()
    my_pagination = Paginator(all_bookings, 5)

    page_number = request.GET.get('page', 1)
    page_obj = my_pagination.page(page_number)
    return render(request, "user_templates/my_bookings.html", {"page_obj": page_obj})


def add_booking(request):
    if request.POST:
        booking_form = BookingForm(request.POST)
        if booking_form.is_valid():
            booking_form.save()

            """ Updating in Rooms db that booked room is non-available"""
            selected_rooms = booking_form.cleaned_data['rooms']
            for my_rooms in selected_rooms:
                get_room_form_db = Rooms.objects.get(id=my_rooms.id)
                get_room_form_db.room_status = "NotAvailable"
                get_room_form_db.save()
            return redirect(view_booking)
    else:
        booking_form = BookingForm()
    return render(request, "user_templates/add_booking.html", {"booking_form": booking_form})


def update_booking(request, update_id):
    booking_tobe_updated = get_object_or_404(Booking, pk=update_id)
    if request.POST:
        booking_form = BookingForm(request.POST, instance=booking_tobe_updated)
        if booking_form.is_valid():
            for blocked_room in booking_tobe_updated.rooms.all():
                blocked_room.room_status = "Available"
                blocked_room.save()
            booking_tobe_updated.rooms.clear()
            booking_form.save()
            for updated_room in booking_form.cleaned_data['rooms']:
                updated_room.room_status = "NotAvailable"
                updated_room.save()
            return redirect(view_booking)
    else:
        booking_form = BookingForm(instance=booking_tobe_updated)
    return render(request, "user_templates/update_booking.html",
                  {"booking_form": booking_form, "update_id": update_id})


def delete_booking(request, delete_id):
    booking_tobe_deleted = get_object_or_404(Booking, pk=delete_id)
    for blocked_room in booking_tobe_deleted.rooms.all():
        blocked_room.room_status = "Available"
        blocked_room.save()
    booking_tobe_deleted.delete()
    return redirect(view_booking)


def view_customer(request):
    all_customers = Customer.objects.all()
    my_pagination = Paginator(all_customers, 5)

    page_number = request.GET.get('page', 1)
    page_obj = my_pagination.page(page_number)
    return render(request, "user_templates/my_customers.html", {"page_obj": page_obj})


def add_customer(request):
    if request.POST:
        customer_form = CustomerForm(request.POST)
        if customer_form.is_valid():
            customer_form.save()
            customer_form = CustomerForm()
            return redirect(view_customer)
    else:
        customer_form = CustomerForm()
    return render(request, "user_templates/add_customer.html", {"customer_form": customer_form})


def update_customer(request, update_id):
    customer_tobe_updated = get_object_or_404(Customer, pk=update_id)
    if request.POST:
        customer_form = CustomerForm(request.POST, instance=customer_tobe_updated)
        if customer_form.is_valid():
            customer_form.save()
            return redirect(view_customer)
    else:
        customer_form = CustomerForm(instance=customer_tobe_updated)
    return render(request, "user_templates/update_customer.html",
                  {"customer_form": customer_form, "update_id": update_id})


def delete_customer(request, delete_id):
    customer_tobe_deleted = get_object_or_404(Customer, pk=delete_id)
    customer_tobe_deleted.delete()
    return redirect(view_customer)
