from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import *
from .forms import *


# Home page
def home(request):
    return render(request, 'home.html')


# About us page
def about_us(request):
    return render(request, 'about_us.html')

def popular_destination(request):
    popular_destinations = PopularDestination.objects.all()
    return render(request, 'popular_destination.html', {'popular_destinations': popular_destinations})

def add_popular_destination(request):
    form = PopularDestinationForm()
    if request.method == 'POST':
        form = PopularDestinationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('popular_destination')
    return render(request, 'popular_destination_form.html', {'form': form})

def delete_popular_destination(request, id):
    popular_destination = PopularDestination.objects.get(pk=id)
    if request.method == 'POST':
        popular_destination.delete()
        return redirect('popular_destination')
    return render(request, 'delete_popular_destination.html')

def update_popular_destination(request, id):
    popular_destination = PopularDestination.objects.get(pk=id)
    form = PopularDestinationForm(instance=popular_destination)
    if request.method == 'POST':
        form = PopularDestinationForm(request.POST, request.FILES, instance=popular_destination)
        if form.is_valid():
            form.save()
            return redirect('popular_destination')
    return render(request, 'popular_destination_form.html', {'form': form})
# Booking page where passenger details are filled
@login_required(login_url='log_in')
def book(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data.copy()
            # Convert date fields to string for session serialization
            if 'departure_date' in cleaned_data and cleaned_data['departure_date']:
                cleaned_data['departure_date'] = cleaned_data['departure_date'].isoformat()
            request.session['booking_info'] = cleaned_data
            request.session['number_of_passengers'] = cleaned_data.get('number_of_passengers')  # Store passenger count
            return redirect('book_transport')  # Ensure this redirect is correct
        else:
            return render(request, 'book.html', {'form': form})  # Re-render form with errors
    else:
        form = BookingForm()
    return render(request, 'book.html', {'form': form})


# Book transport view (after booking form is submitted)
def book_transport(request):
    # Check if booking information is in session
    if 'booking_info' not in request.session:
        return redirect('book')  # If booking info is missing, redirect to the booking form page

    booking_info = request.session.get('booking_info', {})
    mode_of_travel = booking_info.get('mode_of_travel')  # Retrieve mode of travel from session

    # Ensure mode_of_travel is valid and filter transports accordingly
    if mode_of_travel:
        transports = Transport.objects.filter(transport_type=mode_of_travel)  # Filter transports by mode of travel
    else:
        transports = Transport.objects.none()  # No transports if mode_of_travel is missing

    if request.method == 'POST':
        form = TransportSelectionForm(request.POST)
        if form.is_valid():
            request.session['transport_info'] = form.cleaned_data
            return redirect('seat_selection')
    else:
        form = TransportSelectionForm()

    return render(request, 'book_transport.html', {'transports': transports, 'form': form})


# Seat selection view
def seat_selection(request, transport_id):
    transport = Transport.objects.get(id=transport_id)
    seats = Seat.objects.filter(transport=transport, is_booked=False)

    if request.method == 'POST':
        form = SeatSelectionForm(request.POST)
        if form.is_valid():
            selected_seat = form.cleaned_data['seat']
            selected_seat.is_booked = True
            selected_seat.save()

            booking_info = request.session.get('booking_info', {})
            booking = Booking.objects.create(
                user=request.user,
                transport=transport,
                seat=selected_seat,
                passenger_name=booking_info.get('passenger_name'),
                passenger_email=booking_info.get('passenger_email'),
                passenger_address=booking_info.get('passenger_address'),
                passenger_gender=booking_info.get('passenger_gender'),
                number_of_passengers=booking_info.get('number_of_passengers'),
            )
            return redirect('payment', booking_id=booking.id)
    else:
        form = SeatSelectionForm()

    return render(request, 'seat_selection.html', {'transport': transport, 'seats': seats, 'form': form})


# Payment view
def payment(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.booking = booking
            payment.save()
            return redirect('payment_success', booking_id=booking.id)
    else:
        form = PaymentForm()
    return render(request, 'payment.html', {'form': form, 'booking': booking})


# Payment success view after successful payment
def payment_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'payment_success.html', {'booking': booking})


# Print receipt after payment is successful
def print_receipt(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    payment = Payment.objects.filter(booking=booking).first()
    context = {
        'name': booking.passenger_name,
        'phone_number': booking.user.phone_number if booking.user.phone_number else "N/A",
        'from': booking.from_location,  # Use from_location from Booking model
        'to': booking.to_location,      # Use to_location from Booking model
        'seat_number': booking.seat.seat_number,
        'mode_of_travel': booking.transport.transport_type,
    }
    return render(request, 'print_receipt.html', context)


# Passenger Details View (where user provides personal info and selects a seat)
def passenger_details(request, seat_id):
    # Get the seat object by ID
    seat = get_object_or_404(Seat, id=seat_id)

    if request.method == 'POST':
        form = PassengerDetailsForm(request.POST)
        if form.is_valid():
            # Retrieve cleaned data from the form
            passenger_data = form.cleaned_data

            # Create a booking with the form data and selected seat
            booking_info = request.session.get('booking_info', {})
            booking = Booking.objects.create(
                user=request.user,
                transport=seat.transport,
                seat=seat,
                passenger_name=passenger_data['name'],
                passenger_address=passenger_data['address'],
                passenger_gender=passenger_data['gender'],
                number_of_passengers=booking_info.get('number_of_passengers', 1),
            )

            # Mark the seat as booked
            seat.is_booked = True
            seat.save()

            # Redirect to payment page after booking is created
            return redirect('payment', booking_id=booking.id)
    else:
        form = PassengerDetailsForm()

    return render(request, 'passenger_details.html', {'form': form, 'seat': seat})


# Login page
def log_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_management and not user.is_approved:
                form.add_error(None, "Your account is awaiting admin approval.")
            else:
                auth_login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'log_in.html', {'form': form})


# Sign up page
def sign_up(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data.get('role')  
            if role.lower() == 'management':
                user.is_management = True
                user.is_approved = False
            else:
                user.is_approved = True
            user.save()

            group, created = Group.objects.get_or_create(name=role.capitalize())
            user.groups.add(group)

            if user.is_management and not user.is_approved:
                return render(request, 'approval_pending.html')
            else:
                auth_login(request, user)
                return redirect('home')

    else:
        form = CustomUserCreationForm()
    return render(request, 'sign_up.html', {'form': form})

# Custom logout view
def custom_logout(request):
    logout(request)
    return redirect('log_in')
